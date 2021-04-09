from pathlib import Path
import asyncio
import sys
import numpy as np
sys.path.insert(0, str(Path.cwd()))
import pandas as pd
import time
import datetime
import pickle
import os


from saomsg.client import Subscriber


async def main(wheel, goto):

    

    pmac = Subscriber(host="fields", port=10100)
    pows = Subscriber(host="fields", port=10101)
    await pmac.open()
    await pows.open()

    tsk1 = asyncio.create_task( pmac.mainloop() )
    tsk2 = asyncio.create_task( pows.mainloop() )
    await asyncio.sleep(1.0)

    positions = {}
    for number in range(1, 7):
        name = await pmac.get(f"{wheel}Names{number}")
        pos = await pmac.get(f"{wheel}Pos{number}")
        positions[number] = (name, pos)

    msg_vars = (
            "Pos", 
            "HLimBit",
            "ULimBit",
            )

    for v in (msg_vars):

        pmac.subscribe(f"{wheel}{v}", p)

    await asyncio.sleep(0.5)

    #tsk2 = asyncio.create_task( s.run("filter2Wheel", pos, "Abs") )
    resp = await pmac.run( wheel, goto, timeout=30.0 )

    print(resp)


    await pmac.stop()
    await pows.stop()
    await tsk1
    await tsk2




async def test():

    wheels = (
            "filter1Wheel",
            "filter2Wheel",
            "grismWheel",
            )

    positions = [60, 120, 180, 240, 300, 360]
    pmac = Subscriber(host="fields", port=10100)
    await pmac.open()


    tsk1 = asyncio.create_task( pmac.mainloop() )

    await asyncio.sleep(1.0)


    
    data = []
    start = time.time()

    for target in positions:
        for wheel in wheels:
            testpos = np.linspace(target-1, target+1, 50)
            print(f"Moving {wheel} to target {target}")

            for pos in testpos:
                pos = pos%360

                await pmac.run('filter1Wheel', 'H3000')
                print(f"moved {wheel} to test position {pos}")
                p = await pmac.get(f"{wheel}Pos")
                h =await pmac.get(f"{wheel}HLimBit")
                m = await pmac.get(f"{wheel}MLimBit")
                
                awaylima = await pmac.get(f"{wheel}DetentAwayLimA")
                awaylimb = await pmac.get(f"{wheel}DetentAwayLimB")
                awaylima = await pmac.get(f"{wheel}DetentAwayLimA")
                awaylimb = await pmac.get(f"{wheel}DetentAwayLimB")

                nearlima = await pmac.get(f"{wheel}DetentNearLimA")
                nearlimb = await pmac.get(f"{wheel}DetentNearLimB")
                nearlima = await pmac.get(f"{wheel}DetentNearLimA")
                nearlimb = await pmac.get(f"{wheel}DetentNearLimB")

                swhistaway = await pmac.get(f"{wheel}SwitchHistAway")
                swhistnear = await pmac.get(f"{wheel}SwitchHistNear")

                detenttola = await pmac.get(f"{wheel}DetentTolA")
                detenttolb = await pmac.get(f"{wheel}DetentTolB")

                detenttol = await pmac.get(f"{wheel}DetentTol")
                now = time.time()-start

                data.append((
                    now, 
                    float(p[0]), 
                    int(h[0]), 
                    int(m[0]), 
                    wheel, 
                    "positive", 
                    float(awaylima[0] ),
                    float(awaylimb[0] ),
                    float(awaylima[0] ),
                    float(awaylimb[0] ),

                    float(nearlima[0] ),
                    float(nearlimb[0] ),
                    float(nearlima[0] ),
                    float(nearlimb[0] ),

                    float(swhistaway[0] ),
                    float(swhistnear[0] ),

                    float(detenttola[0] ),
                    float(detenttolb[0] ),

                    float(detenttol[0] ),
                    
                    ))
                break
            break
            
            await pmac.run(wheel, target+5, "Abs")

            for pos in reversed(testpos):
                pos = pos%360
                await pmac.run(wheel, pos, "Abs")
                print(f"moved {wheel} to test position {pos}")
                p = await pmac.get(f"{wheel}Pos")
                h = await pmac.get(f"{wheel}HLimBit")
                m = await pmac.get(f"{wheel}MLimBit")
                awaylima = await pmac.get(f"{wheel}DetentAwayLimA")
                awaylimb = await pmac.get(f"{wheel}DetentAwayLimB")
                awaylima = await pmac.get(f"{wheel}DetentAwayLimA")
                awaylimb = await pmac.get(f"{wheel}DetentAwayLimB")

                nearlima = await pmac.get(f"{wheel}DetentNearLimA")
                nearlimb = await pmac.get(f"{wheel}DetentNearLimB")
                nearlima = await pmac.get(f"{wheel}DetentNearLimA")
                nearlimb = await pmac.get(f"{wheel}DetentNearLimB")

                swhistaway = await pmac.get(f"{wheel}SwitchHistAway")
                swhistnear = await pmac.get(f"{wheel}SwitchHistNear")

                detenttola = await pmac.get(f"{wheel}DetentTola")
                detenttolb = await pmac.get(f"{wheel}DetentTolB")

                detenttol = await pmac.get(f"{wheel}DetentTol")
                now = time.time()-start

                now = time.time()-start

                data.append((
                    now, 
                    float(p[0]), 
                    int(h[0]), 
                    int(m[0]), 
                    wheel, 
                    "positive", 
                    float(awaylima[0] ),
                    float(awaylimb[0] ),
                    float(awaylima[0] ),
                    float(awaylimb[0] ),

                    float(nearlima[0] ),
                    float(nearlimb[0] ),
                    float(nearlima[0] ),
                    float(nearlimb[0] ),

                    float(swhistaway[0] ),
                    float(swhistnear[0] ),

                    float(detenttola[0] ),
                    float(detenttolb[0] ),

                    float(detenttol[0] ),
                    
                    ))


        break
    df = pd.DataFrame(data, 
        columns=("time", "pos", "h", 'm', 'wheel',
        'direction',

                "awaylima",
                "awaylimb",
                "awaylima",
                "awaylimb",

                "nearlima",
                "nearlimb",
                "nearlima",
                "nearlimb",

                "swhistaway",
                "swhistnear",

                "detenttola",
                "detenttolb",

                "detenttol",

        ))
    
#    try:
#        now = datetime.datetime.now()
#        fname = now.strftime("%d%b%Y-%H%M%S.pkl")
#        with open(fname, 'wb') as pkl:
#            pickle.dump( df, pkl )
#    except Exception as error:
#        print(error)
#
#    try:
#        await pmac.run("filter1Wheel", 'Y')
#        await pmac.run("filter2Wheel", 'HK3')
#        await pmac.run("grismWheel", 'H3000')
#    except Exception as error:
#        print('Error')

    return df

async def p(val):
    await asyncio.sleep(0.05)
    print(val)


import sys
print(sys.argv)
#asyncio.run(main(*sys.argv[1:]))
#asyncio.run(test())

