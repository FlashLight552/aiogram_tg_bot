import React from "react";
import { Link } from "react-router-dom";

function Home() {
  let services = {
    chumash: "Хумаш",
    tehillim: "Теилим",
    tanya: "Тания",
    hayom_yoma: "Йом йом",
    rambam: "«Книга заповедей» РАМБАМа",
    moshiach: "Мошиах и Освобождение",
  };

  return (
    <div className="home">
      <div className="contentbutton">
        {Object.keys(services).map((key, value) => (
          <Link to={"/" + key} className="button-tg">
            {Object.values(services)[value]}
          </Link>
        ))}
      </div>
    </div>
  );
}

export default Home;
