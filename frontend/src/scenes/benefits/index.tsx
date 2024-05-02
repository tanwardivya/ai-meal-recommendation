import HText from "@/shared/HText";
import { BenefitType, SelectedPage } from "@/shared/types";
import {
    ScaleIcon,
    CalculatorIcon,
    CurrencyDollarIcon,
} from "@heroicons/react/24/solid";
import { motion } from "framer-motion";
import Benefit from "./Benefit";
import ActionButton from "@/shared/ActionButton";
import RABenefitPageGraphic from "@/assets/RABenefitHomePageGraphic.png"

const container = {
    active: {
    },
    inactive: {
      backgroundColor: "#fff",
      transition: { duration: 2 }
    }
  }

type Props = {
    setSelectedPage: (value: SelectedPage) => void;

}
const benefits: Array<BenefitType> = [
    {
        icon: <ScaleIcon className="h-6 w-6"/>,
        title: "Health Condition Adaptability",
        description: 
            "Your health is our priority. Whether you're managing diabetes, high cholesterol, or obesity, our system is equipped to suggest recipes that cater to your specific health needs. By focusing on low glycemic index recipes for diabetics and heart-healthy options for those with high cholesterol, we ensure every meal is a step towards better health."
    },
    {
        icon: <CalculatorIcon className="h-6 w-6"/>,
        title: "Calorie Estimation Accuracy",
        description: 
            "Stay on track with your dietary goals with our accurate calorie content estimations for each recipe. Whether you aim for weight loss, maintenance, or muscle gain, our system aids you in making informed decisions that align perfectly with your objectives."
    },
    {
        icon: <CurrencyDollarIcon className="h-6 w-6"/>,
        title: "Cost-Effective Nutrition",
        description: 
            "Eating well shouldn't break the bank. Our model considers the cost per serving, making Recipe Assistant an invaluable tool for those mindful of their budget. We believe in balancing nutritional value with cost efficiency, ensuring you get the most out of every meal."
    },
]

const Benefits = ({setSelectedPage}: Props) => {
  return (
    <section
        id="benefits"
        className="mx-auto min-h-full w-5/6 py-20">
    <motion.div
     onViewportEnter={() => setSelectedPage(SelectedPage.Benefits)}
    >
        {/* HEADER */}
        <motion.div 
            initial="hidden"
            whileInView="visible"
            viewport={{ once: true, amount: 0.5 }}
            transition={{ duration: 0.5 }}
            variants={{
            hidden: { opacity: 0, x: -50 },
            visible: { opacity: 1, x: 0 },
            }}
            className="md:my-5 md:w-3/5"
        >
            <HText>MEET YOUR CULINARY GENIUS.</HText>
            <p className="my-5 text-sm">
            At Recipe Assistant, we're not just about recipes; we're about creating a healthier, happier you. Our sophisticated Large Language Model (LLM)-based recommendation system is designed to revolutionize your culinary experience by providing personalized, accurate, and beneficial recipe suggestions tailored specifically to you
            </p>
        </motion.div>
        {/* BENEFITS */}
        <motion.div 
         className="md:flex itmes-center justify-between gap-8 mt-5"
         initial="hidden"
         whileInView="visible"
         viewport={{once: true, amount: 0.5}}
         variants={container}
         animate="active"
        >
            {benefits.map((benefit: BenefitType) =>(
                <Benefit 
                    key={benefit.title}
                    icon={benefit.icon}
                    title={benefit.title}
                    description={benefit.description}
                    setSelectedPage={setSelectedPage}
                />
            ))}
        </motion.div>
        {/*  GRAPHICS AND DESCRIPTION */}
        <div className="mt-16 items-center justify-between gap-20 md:mt-28 md:flex">
            {/* GRAPHIC */}
            <img
                className="mx-auto"
                alt = "benefit-page-graphic"
                src={RABenefitPageGraphic}
            />
            {/* DESCRIPTION */}
            <div>
                {/* TITLE */}
                <div className="relative">
                    <div className="before:absolute before:-top-20 before:-left-20 before:z-[1] before:content-abstractwaves">
                        <motion.div
                          initial="hidden"
                          whileInView="visible"
                          viewport={{ once: true, amount: 0.5 }}
                          transition={{ duration: 0.5 }}
                          variants={{
                          hidden: { opacity: 0, x: 50 },
                          visible: { opacity: 1, x: 0 },
                          }}
                        >
                            <HText>DISCOVER THE RECIPE ASSISTANT{" "}
                            <span className="text-primary-500">DIFFERENCE</span>
                            </HText>
                        </motion.div>
                    </div>

                </div>
                {/* DESCRIPTION */}
                <motion.div
                  initial="hidden"
                  whileInView="visible"
                  viewport={{ once: true, amount: 0.5 }}
                  transition={{ delay:0.2, duration: 0.5 }}
                  variants={{
                  hidden: { opacity: 0, x: 50 },
                  visible: { opacity: 1, x: 0 },
                  }}
                >
                    <p className="my-5">
                    Embark on a culinary journey that respects your health, dietary preferences, and wallet. With Recipe Assistant, explore a world of recipes designed just for you. Eat well, live well, and thrive with us by your side.
                    </p>
                    <p className="my-5">
                    Reliability and relevance are at the heart of our recommendations. By benchmarking our system against a human-curated dataset of recipes, we ensure our suggestions match the quality and creativity of expertly crafted meals. This rigorous evaluation process refines our system's accuracy and utility, providing you with choices you can trust.
                    </p>
                </motion.div>
                {/* BUTTON */}
                <div className="relative mt-16">
                    <div className="before:absolute before:-bottom-20 before:right-40 before:z-[-1] before:content-sparkles">
                        <ActionButton setSelectedPage={setSelectedPage}>
                            Join Now
                        </ActionButton>
                    </div>

                </div>
            </div>
            
        </div>

    </motion.div>
    </section>
  );
}

export default Benefits;