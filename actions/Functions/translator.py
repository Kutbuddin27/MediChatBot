response_further_test = {'blood-test':{ 'cbc':['COMPLETE BLOOD COUNT; CBC',' CBC provides information about red cells, white cells and platelets.','350.00','No special preparation required','Daily'],
                                        'rbc':['RED BLOOD CELLS; RBC COUNT','High RBC count maybe caused by low oxygen levels, Polycythemia, kidney disease, dehydration or intake of anabolic steroids. A combination of high or normal RBC count, low MCV & normal RDW is a common pattern in thalassemia trait. Low RBC count leads to anemia either due to decreased production or blood loss.','120.00','No special preparation required','Daily'],},
                       'urine-test':{'RE':['URINE EXAMINATION, ROUTINE; URINE, R/E','Urine analysis is one of the most useful laboratory tests as it identifies a wide range of medical conditions including renal damage, urinary tract infections, diabetes, hypertension and drug toxicity.','120.00','First morning urine sample preferred.','Daily'],
                                     'REA':['URINE EXAMINATION, ROUTINE; URINE R/E, AUTOMATED',' Urine analysis is one of the most useful laboratory tests as it identifies a wide range of medical conditions including renal damage, urinary tract infections, diabetes, hypertension and drug toxicity.This assay is performed on urine sediment by a chemical analyser that is able to detect urine particles in the sediment with high accuracy.','180.00','No special preparation required','Sample Daily by 4 pm; Report Same day'],},
                        'imaging-test':{'mri':['Magnetic Resonance imaging(MRI)','Magnetic resonance imaging, or MRI, is a noninvasive medical imaging test that produces detailed images of almost every internal structure in the human body, including the organs, bones, muscles and blood vessels. MRI scanners create images of the body using a large magnet and radio waves.','4300.00','No special preparation required','Daily'],
                                        'xray':['X-ray','X-rays are a type of radiation called electromagnetic waves. X-ray imaging creates pictures of the inside of your body. The images show the parts of your body in different shades of black and white. This is because different tissues absorb different amounts of radiation.','200.00','No special preparation required','Daily'],},
                                        }
def test_descript(t,t_t,d):
    card_content=''
    for test,typ in d.items():
        if t==test:
            for test_type,card in  typ.items():
                if t_t==test_type:
                      card_content = f"""
                            <b>Name :</b> {card[0]}<br>
                            <b>Description:</b> `{card[1]}`<br>
                            <b>Price :</b> {card[2]}<br>
                            <b>Precondition :</b> {card[3]}<br>
                            <b>Reporting Schedule :</b> {card[4]}<br>
                            """
    return card_content      

# def test_buttons()   