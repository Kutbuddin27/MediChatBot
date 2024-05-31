import mysql.connector as mc

def database_cred(mc):
    # Connect to MySQL
        db = mc.connect(
            host="localhost",
            user="root",
            password="Rasa#098",
            database="medichat"
        )
        return db

def test_descript(t_t):
    card_content=''
    db = database_cred(mc) 
    cursor = db.cursor()
    cursor.execute("SELECT * FROM card WHERE test_t_t =%s",(t_t,))
    data = cursor.fetchall()
    db.close()
    cursor.close()
   
    card_content = f"""
                            <div style='background-color: white; border: 1px solid #e0e0e0; border-radius: 5px; box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1); padding: 16px; margin-bottom: 16px;'>
                            <div style='font-size: 14px; line-height: 1.5;'>
                                <h3 style='margin-top: 0; margin-bottom: 8px; font-size: 18px;'><b>Name:</b> {data[0][2]}</h3>
                                <p style='margin-top: 0; margin-bottom: 8px;'><b>Description:</b> {data[0][3]}</p>
                                <p style='margin-top: 0; margin-bottom: 8px;'><b>Price:</b> {data[0][4]}</p>
                                <p style='margin-top: 0; margin-bottom: 8px;'><b>Precondition:</b> {data[0][5]}</p>
                                <p style='margin-top: 0; margin-bottom: 8px;'><b>Reporting Schedule:</b> {data[0][6]}</p>
                            </div>
                            </div>
                            """
    return card_content      


# print(__package__)

# def test_buttons()   