import os
import flask, json, aiomysql, random
from flask import *
from dotenv import load_dotenv
from hcskr import asyncSelfCheck, QuickTestResult

load_dotenv()
autocheck=Flask(__name__)

@autocheck.route("/")
def index():
    return render_template("index.html")

@autocheck.route("/privacy")
def privacy():
    return render_template("privacy.html")

@autocheck.route("/registration", methods=["POST"])
async def success():
    if request.method=="POST":
        #db set
        db = await aiomysql.connect(host=os.getenv('db_host'), port=os.getenv('db_port'), user=os.getenv('db_us'), password=os.getenv('db_ps'), db=os.getenv('db_database'), charset='utf8')
        cur= await db.cursor()
        result=request.form
        check = await asyncSelfCheck(result["이름"], result["생년월일"], result["지역"], result["학교"], result["학교종류"], result["비밀번호"], quicktestresult=QuickTestResult['none'])
        if check["error"]==False:
            sql = f"SELECT * FROM autocheck WHERE name='{result['이름']}' AND birth='{result['생년월일']}'"
            await cur.execute(sql)
            rows = await cur.fetchall()
            if rows:
                message=f"등록에 실패하였습니다!"
                error_message=f"이미 등록된 학생정보입니다."
                return render_template("result.html", message=message, error_message=error_message)
            else:
                sql2 = f"SELECT COUNT(*) FROM autocheck"
                await cur.execute(sql2)
                result2 = await cur.fetchall()
                #print(result4[0][0])
                result3 = result2[0][0] + 1
                pass
            sql = f'INSERT INTO autocheck(indexrow, name, birth, region, school, schooltype, password) values (%s, %s, %s, %s, %s, %s, %s);'
            await cur.execute(sql, (result3, result['이름'], result['생년월일'], result['지역'], result['학교'], result['학교종류'], result['비밀번호']))
            await db.commit()
            message="성공적으로 등록되었습니다!"
            return render_template("result.html", message=message)
        elif check["error"]==True:
            message=f"등록에 실패하였습니다!"
            return render_template("result.html", result=result, message=message, error_message=check['message'])



if __name__ == '__main__':
    autocheck.run(debug=false)
