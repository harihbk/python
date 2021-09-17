from flask import Flask , Response , jsonify , make_response
import formulas
from flask import request
import requests
import re    
import hotxlfp
import time



app = Flask(__name__)

@app.route('/')
def hello_world():
    start_time = time.time()
    data = requests.get("https://curtainmatrix.co.uk/api/public/api/setting/formula/list").json()
    modified_dict = {}
    for_dict = {}
    vars = [
        { 'MOTOR' : 'Standard Battery 03' , 'WIDTH' : 2000 },
        { 'CONTROLOPTION' : 'Cloth Only' , 'MEASURETO' : 'Fabric Size', 'WIDTH':1000 },
        { 'CONTROLOPTION' : 'Cloth Only', 'LATH_MOTOR_ALLOWANCE' : 12, 'MEASURETO' : 'Fabric Size'  , 'WIDTH' : 13  },
        { 'CONTROLOPTION' : 'Motorised' , 'FINISH' : 'No Sew','MEASUREMENT': 'm' ,  'MEASURETO' : 'Recess', 'WIDTH' : 100},
        { 'CONTROLOPTION' : 'Motorised','MEASUREMENT': 'm' , 'MEASURETO' : 'Recess' , 'WIDTH' : 100},
        {  'MEASURETO' : 'Recess' ,'MOTOR' : 'Standard Battery 03' ,'WIDTH' : 12 }
        ]
    for d in data['result']:
        varabile = d['variablename'].replace(" ","")
        modified_dict[varabile] = "="+d['formula'].replace("if","IF")
       

    for index, item in enumerate(modified_dict):
        fun = formulas.Parser().ast(modified_dict[item])[1].compile()
        checkparameter = list(fun.inputs)
        dict = {}
        for x in checkparameter:
            # Remove Unwanted parameters , if not params error occur
           if vars[index].__contains__(x):
               dict[x] = vars[index][x]
        result = fun(**dict)
        # After Formula calculated result push into dictionary for another formula evaluate
        for_dict[item] = result

        end_time = time.time()
    print(for_dict)

    print(end_time-start_time)
        
    
    formu = """=IF(A1="Standard",
            (Round((IF(B1="Pair",C1*2,C1)*(IF(A1="Standard",
            (D1/10),(E1/10))))/if(F1="mm",G1/10,
            if(F1="inch",(G1*25.4)/10,if(F1="cm",
            (G1*10)/10,G1*100))),1)),H1)"""
    params= {
            "A1":"Standard",
            "B1":"Pair" ,
            "C1":2,
            "D1" :3,
            "E1" :2,
            "F1" :'mm',
            "G1" :12,
            "H1" :12
        }
    c = 0
    fun = formulas.Parser().ast(formu)[1].compile()

    # for index, item in enumerate(listfor):
    #     print(index, item)

   
        

    result = fun(**params)
    
    


    response = make_response(
            jsonify(
                {"result": str(result)}
            ),
            200,
        )
    response.headers["Content-Type"] = "application/json"
    return response


@app.route('/dynamic')
def dynamic():
    
    formula = [
        """=IF(A1 = 1 , IF(B1 = 3 , 3, 4) ,4)""",
        """=IF(A2 = 3 , A2 , 4) + A2""",
        """=IF(A2 = 6 , 12 ,14)"""
    ]

    params = [
    {"A1" : 1 ,"B1" :3 },
    {"A2" : 3 },
    {"A2" : 6 }
    ]

    ch = 'A'
    d = {}
    formuladata = {}
    for index, item in enumerate(formula):
        d[ch + str(2)] = index * 2
        # interchange variable after formula calculate
        vars = d[ch + str(2)]
        
        calculated = formulas.Parser().ast(item)[1].compile()
        checkparameter = list(calculated.inputs)
        
        #Reorder Dictionary what we have in parameters and remove unwanted params[index]
        dict = {}
        for x in checkparameter:
            if params[index].__contains__(x):
                dict[x] = params[index][x]
            
        result = calculated(**dict)
        print(result)
        formuladata[vars] = result
        ch = chr(ord(ch) + 1)
        
    return "s"

@app.route('/api')
def api():
    data = requests.get("https://curtainmatrix.co.uk/api/public/api/setting/formula/list").json()
    modified_dict = {}
    vars = { 'MeasureTo' : 'Fabric Size',
         'ControlOption' : 'Cloth Only',
         'Width' : 12,
        'Width-Lath_Motor_Allowance' : 'none',
         'Measurement' : 'm',
         'Finish' : 'No Sew' ,
         'Width' : 10,
         'Motor' : 'Standard Battery 03'}
    
    
    for d in data['result']:
        varabile = d['variablename'].replace(" ","")
        modified_dict[varabile] = d['formula'].replace("if","IF")
    
    p = hotxlfp.Parser()
    for var in vars:
        p.set_variable(var, vars[var])
   
    for formula in modified_dict:
        dynami_formula = modified_dict[formula]
        data = p.parse(dynami_formula)
        print(dynami_formula)
        print(data)

          
    #print(modified_dict)
    response = make_response(
            jsonify(
                {"result": modified_dict}
            ),
            200,
        )
    return response
   
    
    
    


if __name__ == '__main__':
   app.run()