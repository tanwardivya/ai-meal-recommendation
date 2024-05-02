import { SelectedPage, RecipeType } from "@/shared/types";
import image7 from "@/assets/image7.png";
import image8 from "@/assets/image8.png";
import image9 from "@/assets/image9.png";
import image10 from "@/assets/image10.png";
import image11 from "@/assets/image11.png";
import image12 from "@/assets/image12.png";
import {motion} from "framer-motion";
import HText from "@/shared/HText";
import Class from "./Recipe";

const recipes :Array<RecipeType> =[
  {
    name:"Scrambled Eggs Spinach Feta Recipe",
    description:"fresh spinach, and  Scrambled Eggs with Spinach and Feta is one of my go-to methods for making sure no spinach goes to waste. It’s fast (like, fast enough to make on a weekday), super delish, and makes me feel pampered.",
    image: image7,
  },
  {
    name:"Grilled Chiken salad Orange Vinaigratte",
    description:"Your new favorite salad for summer. Super light and refreshing, it makes the perfect 30-minute dinner.",
    image: image8,
  },
  {
    name:"Apple Crisp",
    description:"This apple crisp recipe is a simple yet delicious fall dessert that's great served warm with vanilla ice cream.Making irresistible apple crisp is surprisingly easy. You just need a good recipe — and that's where we come in! This top-rated apple crisp recipe with a sweet oat topping is sure to satisfy everyone at your table.",
    image: image9,
  },
  {
    name:"Watermelon Popsicle",
    description:"These watermelon popsicles are the perfect treat for a hot summer day. Ice cold, fruity, and refreshing, they’ll cool you off and quench your thirst in one go. They’re also healthy(!) and super easy to make(!), because this watermelon popsicles recipe calls for two simple ingredients: watermelon and lime juice. That’s right! There’s no added sugar, no added coloring, no added anything here. Just fresh fruit!",
    image: image10,
  },
  {
    name:"Homemade Banana Pudding",
    description:"This Homemade Banana Pudding recipe is a classic Southern dessert made with layers of sliced fresh bananas, an easy homemade custard, Nilla wafers, and topped with a light and fluffy meringue! It's the perfect way to finish any Southern meal!",
    image: image11,
  },
  {
    name:"Grilled Vegetable Salad",
    description:"This Grilled Vegetable Salad Recipe is the absolute BEST! Kalamata olives, artichokes, and feta cheese add a Mediterranean flair. Dressing the salad while it's still warm with Lemon Garlic Vinaigrette just rounds everything out perfectly. This recipe is quick and easy, perfect for a crowd or for epic leftovers!",
    image: image12,
  },
]


type Props = {
  setSelectedPage: (value: SelectedPage) => void;
};

const OurRecipes = ({ setSelectedPage }: Props) => {
  return (
    <section id="ourrecipes" className="w-full bg-primary-100 py-40">
      <motion.div
        onViewportEnter={() => setSelectedPage(SelectedPage.OurRecipes)}
      >
        <motion.div
          className="mx-auto w-5/6"
          initial="hidden"
          whileInView="visible"
          viewport={{ once: true, amount: 0.5 }}
          transition={{ duration: 0.5 }}
          variants={{
            hidden: { opacity: 0, x: -50 },
            visible: { opacity: 1, x: 0 },
          }}
        >
          <div className="md:w-3/5">
            <HText>OUR RECIPES</HText>
            <p className="py-5">
            Explore a world of flavors with Recipe Assistant, where innovation meets tradition in every dish. Our recipes, crafted by advanced LLM technology, are tailored to fit your dietary needs and culinary curiosity. Dive into a personalized cooking experience that transforms ingredients into gourmet adventures, effortlessly.
            </p>
          </div>
        </motion.div>
        <div className="mt-10 h-[353px] w-full overflow-x-auto overflow-y-hidden">
          <ul className="w-[2800px] whitespace-nowrap">
            {recipes.map((item: RecipeType, index) => (
              <Class
                key={`${item.name}-${index}`}
                name={item.name}
                description={item.description}
                image={item.image}
              />
            ))}
          </ul>
        </div>
      </motion.div>
    </section>
  );
};

export default OurRecipes;