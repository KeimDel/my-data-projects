# 👨‍👩‍👧‍👦 Generating Insights for Qatar Airways using AI

> 🚧 Status: Finished (Top 10 Finalist)

---

## 🧾 Overview

In this competition, we created an infographic and developed a topic clustering model using Latent Dirichlet Allocation (LDA) to **identify how airline reviews could be grouped into distinct topics or themes**. The main objective was to generate insights for Qatar Airways and recommend future actions based on those insights.

---

## 📃 Insights

![User Data](./documentation/FP-14_AI_KaryaInfografis_Deluna_page-0001.jpg) 

Insights:

1. Exploratory Data Analysis

We visualized Qatar Airways’ average monthly rating based on reviews from 2014 to 2024. The results show a declining trend starting around 2020. This may suggest a drop in overall customer satisfaction.

2. LDA Analysis

We focused on low-rating passenger reviews (scores of 1 to 4 out of 10) and applied a method called Latent Dirichlet Allocation (LDA) to group them into three main topics:

- **Topic 1**
Keywords: Business, Class, Lounge, Staff, Food, Serve
Interpretation: This topic likely refers to in-flight experiences, including the quality of business class service and meals.

- **Topic 2**
Keywords: Book, Change, Customer, Ticket, Cancel, Refund
Interpretation: This topic highlights issues related to booking, such as ticket changes, cancellations, and refund problems.

- **Topic 3**
Keywords: Delayed, Hotel, Arrive, Staff, Connect, Luggage
Interpretation: This topic appears to focus on delays, missed connections, and baggage handling.

Trends:
- Starting in 2021, there was an increasing trend in the frequency of Topic 1 reviews, indicating growing dissatisfaction with in-flight experiences such as business class service, lounge quality, staff behavior, and food.

- Topic 2 and Topic 3 reviews peaked in 2022, suggesting that issues related to booking (Topic 2) and flight delays or luggage problems (Topic 3) were most prominent during that year. Although both topics saw a decline in 2023, their spike in 2022 highlights a critical period for customer service concerns.

---

3. Future Suggestion

- Personalized Cabin Experience
Enhances passenger comfort through preferred meals, customized entertainment, and real-time seat feedback.

- Real-Time Delay Compensation
Provides automatic compensation, arranges alternative connections, and tracks baggage in real-time during delays.

- Automated Customer Resolution
Offers real-time ticket availability, automatic refund or rebooking, and timely schedule change notifications.


---

## Source Code
- **Topic_Clustering_LDA.ipnyb**

---

## Documentation
- Infographic
- Finalist Certificate

---

## Tools
- Data manipulation & analysis: `pandas`, `numpy`
- Data visualization: `matplotlib`, `seaborn`, `WordCloud`
- Text processing & NLP: `nltk`, `re`, `string`, `collections`
- Topic modeling: `gensim` (LDA), `sklearn.feature_extraction.text`



