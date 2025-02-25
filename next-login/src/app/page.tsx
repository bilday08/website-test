import Image from "next/image";
import styles from "./page.module.css";

export default function Home() {
  return (
    <div className={styles.page}>
      <main className={styles.main}>
        <ol>
          <li>
            Start by running the command <code>npm run dev</code>.
          </li>
          <li>Navigate to pages like login or sign-up.</li>
          <li>Below are the links to the detailed documentation.</li>
        </ol>

        <div className={styles.ctas}>
          <a
            href="https://docs.google.com/document/d/1q9dswhwl6HjPlVDf5gEN-zg_p1Bb9kQBG0r2yI7Ytyk/edit?usp=sharing"
            target="_blank"
            rel="noopener noreferrer"
            className={styles.secondary}
          >
            Read our docs
          </a>
        </div>
      </main>
      <footer className={styles.footer}>
        <a
          href="http://localhost:3000/login"
          target="_blank"
          rel="noopener noreferrer"
        >
          <Image
            aria-hidden
            src="/globe.svg"
            alt="Globe icon"
            width={16}
            height={16}
          />
          Sign In →
        </a>
        <a
          href="http://localhost:3000/sign-up"
          target="_blank"
          rel="noopener noreferrer"
        >
          <Image
            aria-hidden
            src="/globe.svg"
            alt="Globe icon"
            width={16}
            height={16}
          />
          Sign Up →
        </a>
      </footer>
    </div>
  );
}
