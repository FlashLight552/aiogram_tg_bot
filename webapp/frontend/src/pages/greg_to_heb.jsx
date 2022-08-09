import React from "react";
import { useEffect } from "react";


function Gregorian() {
  const monthName = {
    "Январь": "01",
    "Февраль": "02",
    "Март": "03",
    "Апрель": "04",
    "Май": "05",
    "Июнь": "06",
    "Июль": "07",
    "Август": "08",
    "Сентябрь": "09",
    "Октябрь": "10",
    "Ноябрь": "11",
    "Декабрь": "12",
  };

    let month = ("0" + (new Date().getMonth() + 1)).slice(-2);
    let day = ("0" + new Date().getDay()).slice(-2);
    let year = new Date().getFullYear();

    const tg = window.Telegram.WebApp;
    
    useEffect(() => {
        tg.ready();
        tg.MainButton.text = "Конвертировать в Еврейский";
        tg.MainButton.show();
    });

    useEffect(()=>{
        tg.onEvent('mainButtonClicked', function(){
            let date = document.getElementById('gd').value;
            let mounth = document.getElementById('gm').value;
            let year = document.getElementById('gy').value;
            let sunset = document.getElementById('gs').checked;
            tg.sendData('gregorian-'+date+'-'+mounth+'-'+year+'-'+sunset); });
    })

  return (
    <div className="gregorian_to_hebrew">
      <form className="row gy-1 gx-2 mb-3 align-items-center">
        <div className="form-floating col-auto mb-2">
          <input
            type="text"
            className="form-control"
            name="gd"
            placeholder="День"
            size="5"
            defaultValue={day}
            maxLength="2"
            id="gd"
          />
          <label htmlFor="gd">День</label>
        </div>
        <div className="form-floating col-auto mb-2">
          <select name="gm" id="gm" className="form-select" defaultValue={month}>
            {Object.keys(monthName).map((name, value) => (
                  <option key={name} value={Object.values(monthName)[value]} >
                    {name}
                  </option>
                ))}
          </select>
          <label htmlFor="gm">Месяц</label>
        </div>
        <div className="form-floating col-auto mb-2">
          <input
            type="text"
            className="form-control"
            name="gy"
            placeholder="Год"
            defaultValue={year}
            size="5"
            maxLength="4"
            id="gy"
            pattern="-?\d*"
          />
          <label htmlFor="gy">Год</label>
        </div>
        
          <div className="form-check">
            <input className="form-check-input" type="checkbox" name="gs" id="gs" />
            <label className="form-check-label" htmlFor="gs">
              После заката солнца
            </label>
        </div>
      </form>
    </div>
  );
}

export default Gregorian;
