import "./Header.css";
import { AiOutlineHome } from "react-icons/ai";
import { useNavigate } from "react-router";

const Header = () => {
  const nav = useNavigate();
  const homeButtonClickHandler = () => {
    return nav("/");
  };

  return (
    <div className="header_main_frame">
      <div className="header_left_panel_wrapper">
        <button className="home_button" onClick={homeButtonClickHandler}>
          <AiOutlineHome />
        </button>
      </div>
      <div className="header_center_panel_wrapper">좋은 하루 되세요!</div>
    </div>
  );
};

export default Header;
