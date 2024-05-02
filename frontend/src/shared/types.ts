export enum SelectedPage {
    Home = "home",
    Benefits = "benefits",
    OurRecipes = "ourrecipes",
    ContactUs = "contactus",
    Register = "register"
  }

  export interface BenefitType{
    icon: JSX.Element;
    title: string;
    description: string;
  }
  export interface RecipeType {
    name: string;
    description?: string;
    image: string;
  }