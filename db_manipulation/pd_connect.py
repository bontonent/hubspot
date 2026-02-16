import psycopg2
from datetime import datetime
import os
from dotenv import load_dotenv
from pymongo.synchronous import database
import md_connect # Ваш файл з підключенням до MongoDB
from pprint import pprint
import hashlib
from tqdm import tqdm

load_dotenv()

def connect_to_db():
    conn = psycopg2.connect(
        dbname=os.getenv('db_name'),
        user=os.getenv('db_user'),
        password=os.getenv('db_password'),
        port=os.getenv('db_port'),
        host=os.getenv('db_host')
    )
    return conn



def safe_int_hash(value, mod=1_000_000_000):
    h = hashlib.sha256(str(value).encode()).hexdigest()
    return int(h, 16) % mod

def get_month_fields(timestamp_ms):
    dt = datetime.fromtimestamp(timestamp_ms / 1000.0)
    
    month_str = dt.strftime("%Y-%m")
    dim_month_id = safe_int_hash(month_str) 

    year = dt.year
    mouth = dt.month # назва згідно з вашою діаграмою
    mounth_name = dt.strftime("%B")
    quarter = f"Q{(dt.month - 1) // 3 + 1}"
    
    return (dim_month_id, year, mouth, mounth_name, quarter)


# Create data warehouse
# Connect
db = md_connect.connect()
conn = connect_to_db()
cur = conn.cursor()

# get data from credential
data_from_credentials = md_connect.vc_credentials(db)

for data_from_credential in data_from_credentials:
    cur.execute("""
        INSERT INTO dim_credential
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
    """, (
        data_from_credential["_id"],
        data_from_credential.get("internalName")
    ))
    conn.commit()

# Commit ones
cur.execute("""
    INSERT INTO dim_locations (dim_region_id, location_name, locality)
    VALUES (%s,%s,%s)
    ON CONFLICT DO NOTHING
""", (
    0,
    None,
    None
))
conn.commit()

# get data from services
data_from_services =  md_connect.vc_services(db)
for data_from_service in data_from_services:
    cur.execute("""
        INSERT INTO dim_service
        VALUES (%s, %s)
        ON CONFLICT DO NOTHING
    """, (
        data_from_service['_id'],
        data_from_service["name"]
    ))
    conn.commit()

for i_dfp, data_from_product in enumerate(tqdm(md_connect.vc_products(db))):

    product_id = data_from_product["_id"]

    # ---------- LOCATION (беремо першу)
    data_add = {
    "location" : True}

    dim_region_id = None
    if data_from_product.get("locations"):
        try:
            loc = data_from_product["locations"][0]
            dim_region_id = safe_int_hash(
                (loc.get("state"), loc.get("locality"))
            )
            cur.execute("""
                INSERT INTO dim_locations (dim_region_id, location_name, locality)
                VALUES (%s,%s,%s)
                ON CONFLICT DO NOTHING
            """, (
                dim_region_id,
                loc.get("state"),
                loc.get("locality")
            ))
            conn.commit()
        except Exception as e:
            conn.rollback()
            data_add["location"] = False
            print("Don't have locality",e)
    try:
        # ---------- PRODUCT (CORE DIM)
        if data_add["location"]:
            cur.execute("""
                INSERT INTO dim_products (
                    products_id,
                    dim_region_id,
                    product_name,
                    product_tier,
                    partner_type
                )
                VALUES (%s,%s,%s,%s,%s)
                ON CONFLICT DO NOTHING
            """, (
                product_id,
                dim_region_id,
                data_from_product.get("name"),
                data_from_product.get("tier"),
                data_from_product.get("partnerType")
            ))
        else:
            cur.execute("""
                INSERT INTO dim_products (
                    products_id,
                    dim_region_id,
                    product_name,
                    product_tier,
                    partner_type
                )
                VALUES (%s,%s,%s,%s,%s)
                ON CONFLICT DO NOTHING
            """, (
                product_id,
                0,
                data_from_product.get("name"),
                data_from_product.get("tier"),
                data_from_product.get("partnerType")
            ))
    except Exception as e:
        conn.rollback()
        print("Products :", e)

    # ---------- BRIDGE: SERVICE
    for sid in data_from_product.get("catalogServices", []):
        bridge_id = safe_int_hash((product_id, sid))
        try:
            cur.execute("""
                INSERT INTO bridge_product_service (
                    bridge_product_service_id,
                    dim_products_id,
                    dim_service_id
                )
                VALUES (%s,%s,%s)
                ON CONFLICT DO NOTHING
            """, (bridge_id, product_id, sid))
            conn.commit()
        except Exception as e:
            conn.rollback()
            try:
                cur.execute("""
                    INSERT INTO dim_service
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                """, (
                    sid,
                    None
                ))
                conn.commit()

                cur.execute("""
                    INSERT INTO bridge_product_service (
                        bridge_product_service_id,
                        dim_products_id,
                        dim_service_id
                    )
                    VALUES (%s,%s,%s)
                    ON CONFLICT DO NOTHING
                """, (bridge_id, product_id, sid))
                conn.commit()
            except Exception as e:
                conn.rollback()
                print("bridge services:",e)

    # ---------- BRIDGE: CREDENTIAL
    for cid in data_from_product.get("credentials", []):
        bridge_id = safe_int_hash((product_id, cid))
        try:
            cur.execute("""
                INSERT INTO bridge_product_credential (
                    bridge_product_credential_id,
                    dim_products_id,
                    dim_credential_id
                )
                VALUES (%s,%s,%s)
                ON CONFLICT DO NOTHING
            """, (bridge_id, product_id, cid))
            conn.commit()
        
        except Exception as e:
            conn.rollback()
            try:
                cur.execute("""
                    INSERT INTO dim_credential
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                """, (
                    cid,
                    None
                ))
                conn.commit()

                cur.execute("""
                    INSERT INTO bridge_product_credential (
                        bridge_product_credential_id,
                        dim_products_id,
                        dim_credential_id
                    )
                    VALUES (%s,%s,%s)
                    ON CONFLICT DO NOTHING
                """, (bridge_id, product_id, cid))
                conn.commit()
            
            except Exception as e:
                conn.rollback()
                print("bridnge credentials:",e)

    # ---------- ОБРОБКА КОМЕНТАРІВ
    if not data_from_product.get("comment"):
        continue

    comment_group = {}

    for c in data_from_product["comment"]:
        lang = c.get("originalLanguage")
        rating = c.get("ratings", {}).get("OVERALL")

        if rating is None:
            continue

        # Отримуємо дані календаря
        month_data = get_month_fields(c["createdAt"])
        dim_month_id = month_data[0]

        # Отримуємо дані компанії
        reviewer_info = c.get("reviewerData", {})
        c_id = reviewer_info.get("portalId")
        # if c_id:
        #     c_id = 0
        conn.commit()
        # Записуємо в dim_mounth
        cur.execute("""
            INSERT INTO dim_mounth
            VALUES (%s,%s,%s,%s,%s) ON CONFLICT DO NOTHING
        """, month_data)
        conn.commit()

        # Записуємо в dim_language
        lang_id = safe_int_hash(lang)
        cur.execute("""
            INSERT INTO dim_language (dim_language_id, original_language)
            VALUES (%s,%s) ON CONFLICT DO NOTHING
        """, (lang_id, lang))
        conn.commit()

        # Записуємо в dim_company
        if c_id:
            cur.execute("""
                INSERT INTO dim_company (dim_company_id, company_name)
                VALUES (%s,%s) ON CONFLICT DO NOTHING
            """, (c_id, reviewer_info.get("companyName")))
            conn.commit()

        # КЛЮЧ ГРУПУВАННЯ: додаємо c_id, щоб він був доступний після циклу
        key = (dim_month_id, lang, c_id)

        if key not in comment_group:
            comment_group[key] = []
        comment_group[key].append(rating)

    # ---------- ЗАПИС У ТАБЛИЦЮ ФАКТІВ (Comment)
    for (m_id, lang_str, comp_id), rates in comment_group.items():
        try:
            cur.execute("""
            INSERT INTO fact_comment (
                dim_month_id,
                dim_product_id,
                dim_company_id,
                dim_language_id,
                comment_count,
                min_rating,
                avg_rating,
                max_rating
            )
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
            ON CONFLICT (
                dim_month_id,
                dim_product_id,
                dim_company_id,
                dim_language_id
            )
            DO UPDATE SET
                comment_count = EXCLUDED.comment_count,
                min_rating = EXCLUDED.min_rating,
                avg_rating = EXCLUDED.avg_rating,
                max_rating = EXCLUDED.max_rating
            """, (
                m_id,
                product_id,
                comp_id,          # Якщо тут None, а в SQL це FK — може бути помилка
                safe_int_hash(lang_str),
                len(rates),
                min(rates),
                round(sum(rates) / len(rates), 2),
                max(rates)
            ))
            conn.commit() # Зберігаємо, якщо все ок
        except psycopg2.errors.ForeignKeyViolation as e:
            conn.rollback()
            print(f"Ігнорую коментар: одного з ключів не існує в вимірах. Error: {e.pgcode}")
            conn.rollback() 
        except Exception as e:
            conn.rollback()
            
            print(f"Інша помилка при записі факту: {e}")
            conn.rollback()


conn.commit()
cur.close()
conn.close()
