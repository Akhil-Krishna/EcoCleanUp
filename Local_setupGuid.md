

You must create the database first.

---
# ✅ Correct Order (Very Important)

## 1. create .venv

Run:

```bash
python -m venv .venv
```

## 2.Activate .venv

Run:

```bash
.venv\Scripts\activate
```

## 3.install libs

Run:

```bash
pip install -r requirements.txt
```

---
# Next (Very Important)

## Step 1 — Connect to default postgres database

Run:

```bash
psql -U postgres -d postgres
```

(Notice we connect to `postgres`, NOT `ecocleanup_db`)

---

## Step 2 — Create your database

Inside psql:

```sql
CREATE DATABASE ecocleanup_db;
```

You should see:

```
CREATE DATABASE
```

Then exit:

```sql
\q
```

---

## Step 3 — Now run your SQL files

Now this will work:

```bash
psql -U postgres -d ecocleanup_db -f create_database.sql
```

Then:

```bash
psql -U postgres -d ecocleanup_db -f populate_database.sql
```

---

# ✅ Why This Happened

Your command was:

```bash
psql -U postgres -d ecocleanup_db -f create_database.sql
```

But PostgreSQL said:

> I can’t connect to ecocleanup_db because it doesn’t exist.

So you must create it first from another database (usually `postgres`).

---

# 🎯 After That

Update your `connect.py` for local:

```python
def get_connection():
    import psycopg2
    conn = psycopg2.connect(
        host='localhost',
        port=5432,
        database='ecocleanup_db',
        user='postgres',
        password='root'
    )
    return conn
```

---

# 🚀 Quick Check

After running both SQL files successfully, test:

```bash
psql -U postgres -d ecocleanup_db
```

Then:

```sql
\dt
```

If you see tables → 🎉 Your local DB is fully ready.

---
