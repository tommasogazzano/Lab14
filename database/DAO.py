from database.DB_connect import DBConnect
from model.arco import Arco
from model.order import Order
from model.store import Store


class DAO():
    @staticmethod
    def DAOgetStores():
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary = True)
        result = []

        query = '''select s.* 
                    from stores s '''

        cursor.execute(query)
        for row in cursor:
            result.append(Store(**row))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def DAOgetEdges(store_id, maxGiorni, idMap):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []

        query = '''select o1.order_id as oo1, o2.order_id as oo2, SUM(oi1.quantity) + SUM(oi2.quantity) AS peso
                    from orders o1, orders o2, order_items oi1, order_items oi2 
                    where o1.store_id = o2.store_id and o2.store_id = %s and o2.order_date < o1.order_date
                    AND oi1.order_id = o1.order_id AND oi2.order_id = o2.order_id
                    and datediff(o1.order_date,o2.order_date ) < %s
                    GROUP BY 
                        o1.order_id, o2.order_id'''

        cursor.execute(query, (store_id, maxGiorni))
        for row in cursor:
            result.append(Arco(idMap[row["oo1"]], idMap[row["oo2"]], row["peso"]))

        cursor.close()
        conn.close()
        return result

    @staticmethod
    def DAOgetNodes(store_id):
        conn = DBConnect.get_connection()
        cursor = conn.cursor(dictionary=True)
        result = []

        query = '''select *
                        from orders o 
                        where o.store_id  = %s'''

        cursor.execute(query, (store_id,))
        for row in cursor:
            result.append(Order(**row))

        cursor.close()
        conn.close()
        return result
