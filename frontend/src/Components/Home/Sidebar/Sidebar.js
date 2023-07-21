import "./Sidebar.css";
import React from "react";
import { SidebarData } from "./Sidebardata";

export default function Sidebar({ onRouteChange, onInternalRouteChange }) {
  return (
    <div className="sidebar">
      <div className="title">
        <div className="logo"></div>
        <h2>Sercuit</h2>
      </div>
      {SidebarData.map((item, index) => {
        return (
          <ul key={index}>
            {item.title === "Signout" ? (
              <li
                key={index}
                className={item.cName}
                onClick={() => onRouteChange("signin")}
              >
                <div>
                  {item.icon}
                  <span>{item.title}</span>
                </div>
              </li>
            ) : (
              <li
                key={index}
                className={item.cName}
                onClick={() => onInternalRouteChange(`${item.title}`)}
              >
                <div>
                  {item.icon}
                  <span>{item.title}</span>
                </div>
              </li>
            )}
          </ul>
        );
      })}
    </div>
  );
}
