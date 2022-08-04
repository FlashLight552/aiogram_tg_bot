import React from "react";
import { useEffect, useState } from "react";

function Hebrew() {
  const month_name = {
    Нисан: "Нисан",
    Ияр: "Iyyar",
    Сиван: "Sivan",
    Тамуз: "Tamuz",
    Ав: "Av",
    Элул: "Elul",
    Тишрей: "Tishrei",
    Хешван: "Cheshvan",
    Кислев: "Kislev",
    Тевет: "Tevet",
    Шват: "Sh'vat",
    Адар: "Adar",
    "Адар I": "Adar I",
    "Адар II": "Adar II",
  };

  let month = ("0" + (new Date().getMonth() + 1)).slice(-2);
  let day = ("0" + new Date().getDay()).slice(-2);
  let year = new Date().getFullYear();

  const tg = window.Telegram.WebApp;

  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [items, setItems] = useState([]);
  useEffect(() => {
    let url =
      "https://www.hebcal.com/converter?cfg=json&date="+year+"-"+month+"-"+day+"&g2h=1&strict=1";
    fetch(url)
      .then((res) => res.json())
      .then(
        (result) => {
          setIsLoaded(true);
          setItems(result);
        },
        // Note: it's important to handle errors here
        // instead of a catch() block so that we don't swallow
        // exceptions from actual bugs in components.
        (error) => {
          setIsLoaded(true);
          setError(error);
        }
      );
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, []);

  useEffect(() => {
    tg.ready();
    tg.MainButton.text = "Конвертировать в Григорианский";
    tg.MainButton.show();
  });

  useEffect(() => {
    tg.onEvent("mainButtonClicked", function () {
      let date = document.getElementById("gd").value;
      let mounth = document.getElementById("gm").value;
      let year = document.getElementById("gy").value;
      tg.sendData("hebrew-" + date + "-" + mounth + "-" + year);
    });
  });

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
            defaultValue={items.hd}
            maxLength="2"
            id="gd"
          />
          <label htmlFor="gd">День</label>
        </div>
        <div className="form-floating col-auto mb-2">
          <select
            name="gm"
            id="gm"
            className="form-select"
            defaultValue={items.hm}
            key={items.hm}
          >
            {Object.keys(month_name).map((name, value) => (
              <option key={name} value={Object.values(month_name)[value]}>
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
            defaultValue={items.hy}
            size="5"
            maxLength="4"
            id="gy"
            pattern="-?\d*"
          />
          <label htmlFor="gy">Год</label>
        </div>
      </form>
    </div>
  );
}

export default Hebrew;
