import Navbar from "@/scenes/navbar";
import Home from '@/scenes/home';
import Benefits from '@/scenes/benefits';
import OurRecipes from "@/scenes/ourrecipes";
import ContactUs from "@/scenes/contactus";
import { useEffect, useState } from "react";
import { SelectedPage } from "@/shared/types";

type Props = {
};

const Landing = ({}: Props) => {
    const [isTopOfPage, setIsTopOfPage] = useState<boolean>(true);
    const [selectedPage, setSelectedPage] = useState<SelectedPage>(SelectedPage.Home);

  useEffect(()=>{
    const handleScroll = ()=> {
      if (window.scrollY === 0){
        setIsTopOfPage(true);
        setSelectedPage(SelectedPage.Home);
      };
      if (window.scrollY !== 0) setIsTopOfPage(false);
    }
    window.addEventListener("scroll", handleScroll);
    return() => window.removeEventListener("scroll", handleScroll);
  }, []);
  return (
      <div className="landing bg-gray-20">
        <Navbar
          isTopOfPage = {isTopOfPage}
          selectedPage={selectedPage}
          setSelectedPage={setSelectedPage}
        />
        <Home setSelectedPage={setSelectedPage}/>
        <Benefits setSelectedPage={setSelectedPage}/>
        <OurRecipes setSelectedPage={setSelectedPage}/>
        <ContactUs setSelectedPage= {setSelectedPage}/>
      </div>
  );
}

export default Landing