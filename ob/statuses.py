from ob.utils import hub_conn

# schema: https://github.com/auburnsummer/rd-indexer/blob/main/sql/levels.sql
def get_status(id):
    with hub_conn() as conn:
        curr = conn.execute("SELECT * FROM status WHERE id = ?", [id])
        return curr.fetchone()

def set_status(id, obj):
    pass