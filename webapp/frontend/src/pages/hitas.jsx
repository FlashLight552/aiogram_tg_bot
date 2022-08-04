import React from "react";
import { useState } from "react";
import { useEffect } from "react";
import { Link } from "react-router-dom";
import parse from "html-react-parser";  
import Skeleton, { SkeletonTheme } from 'react-loading-skeleton'
import 'react-loading-skeleton/dist/skeleton.css'

function Hitas({ title }) {
  const [error, setError] = useState(null);
  const [isLoaded, setIsLoaded] = useState(false);
  const [items, setItems] = useState([]);

  // Note: the empty deps array [] means
  // this useEffect will run once
  useEffect(() => {
    let url = "https://api.koleltora.pp.ua/api/hitas/" + title;
    // let url = "http://127.0.0.1:8000/api/hitas/" + title;
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

  function open_source() {
    const tg = window.Telegram.WebApp;
    tg.ready();
    tg.openLink("https://moshiach.ru/");
  }

  if (error) {
    return <div>Error: {error.message}</div>;
  } else if (!isLoaded) {
    return (
        <div>
          <SkeletonTheme>
            <p><Skeleton count={1} /></p>
          </SkeletonTheme>
          <SkeletonTheme height='50px'>
            <p><Skeleton count={1} /></p>
          </SkeletonTheme>
          <p><Skeleton count={40} /></p>
        </div>
      
    );
  } else {
    return (
      <div>
        <div className="date">{parse(items.date) || <Skeleton />}</div>
        <div className="title">{parse(items.title) || <Skeleton />}</div>
        <div className="text">{parse(items.text) || <Skeleton />}</div>

        <div>
          <Link to={"/"} className="button-tg">
            Назад
          </Link>
        </div>

        <div className="source">
          Источник:
          <button onClick={open_source} className="source_btn">
            moshiach.ru
          </button>
        </div>
      </div>
    );
  }
}

export default Hitas;
