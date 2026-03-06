from flask_restful import Resource, request
import db as conn
from flask import Flask
from flask_cors import CORS
from flask_restful import Api

app = Flask(__name__)
api = Api(app)

CORS(app)


class GetAvailableSlots(Resource):
    def get(self):
       
        try:
            connection = conn.db_connection()


            cur = connection.cursor()

            cur.execute("SELECT id, slot_time FROM slots WHERE is_booked = FALSE")

            rows = cur.fetchall()

            data = []

            for i in rows:
                data.append({
                    "id": i[0],
                    "slot_time": i[1]
                })

            cur.close()
            connection.close()
            return {"res_status": True, "available_slots": data}

        except Exception as e:
            return {"res_status": False, "msg": str(e)}


class BookSlot(Resource):
    def post(self):
     
        try:
            data = request.get_json()

            slot_id = data.get("slot_id")
            name = data.get("name")

            connection = conn.db_connection()


            cur = connection.cursor()

            cur.execute(
                "UPDATE slots SET is_booked = TRUE, booked_by = %s WHERE id = %s AND is_booked = FALSE",
                (name, slot_id)
            )

            connection.commit()

            if cur.rowcount == 0:
                return {"res_status": False, "msg": "Slot already booked"}

            cur.close()
            connection.close()

            return {"res_status": True, "msg": "Slot booked successfully"}

        except Exception as e:
            return {"res_status": False, "msg": str(e)}

        


class GetBookedSlots(Resource):
    def get(self):
        
        try:
            connection = conn.db_connection()

            if not connection:
                return {"res_status": False, "msg": "Database Connection Failed"}

            cur = connection.cursor()

            cur.execute("SELECT slot_time, booked_by FROM slots WHERE is_booked = TRUE")

            rows = cur.fetchall()

            data = []

            for i in rows:
                data.append({
                    "slot_time": i[0],
                    "booked_by": i[1]
                })

            cur.close()
            connection.close()
            return {"res_status": True, "booked_slots": data}

        except Exception as e:
            return {"res_status": False, "msg": str(e)}

    



api.add_resource(GetAvailableSlots, "/get_slots")
api.add_resource(BookSlot, "/book_slot")
api.add_resource(GetBookedSlots, "/booked_slots")


if __name__ == "__main__":
    app.run(host="localhost", port=5050)