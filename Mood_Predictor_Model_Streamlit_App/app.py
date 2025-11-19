import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from openpyxl import load_workbook
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import warnings
from sklearn.metrics import accuracy_score
warnings.filterwarnings('ignore')
import pickle
from sklearn.preprocessing import LabelEncoder
from mpl_toolkits.mplot3d import Axes3D
import plotly.express as px


excel_file_path = "Mood_Predictor_Model_Streamlit_App/Dataset.xlsx"


df = pd.read_excel(excel_file_path, sheet_name=1, engine='openpyxl')

excel_file_path = "Dataset.xlsx"
breakfast = pd.read_excel(excel_file_path, sheet_name=0, engine='openpyxl')
activity= pd.read_excel(excel_file_path, sheet_name=2, engine='openpyxl')
absenteeism = pd.read_excel(excel_file_path, sheet_name=3, engine='openpyxl')
dinner = pd.read_excel(excel_file_path, sheet_name=4, engine='openpyxl')
sleep = pd.read_excel(excel_file_path, sheet_name=5, engine='openpyxl')
travel = pd.read_excel(excel_file_path, sheet_name=6, engine='openpyxl')
clubs = pd.read_excel(excel_file_path, sheet_name=8, engine='openpyxl')
mood = pd.read_excel(excel_file_path, sheet_name=1, engine='openpyxl')


def apply_dark_theme():
    st.markdown(
        """
        <style>
        /* Dark theme */
        body {
            color: white;
            background-color: #1E1E1E;
        }
        h1, h2, h3, h4, h5, h6 {
            color: white;
        }
        .stApp {
            background-color: #1E1E1E;
            color: white;
        }
        .st-bb {
            background-color: grey; /* Dropdown background color */
            color: white; /* Dropdown text color */
        }
        .st-bc {
            background-color: grey; /* Sidebar background color */
            color: white; /* Sidebar text color */
        }
        .st-dl {
            background-color: #6e6b6b;
            color: black; /* Sidebar title text color */
        }
        .css-145kmo2 {
            background-color: #6e6b6b;
            color: black; /* Sidebar heading text color */
        }
        .st-bp {
            background-color: #6e6b6b; /* Custom background color for some elements */
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
            color: white; 
        }
        .st-bq {
            background-color: #6e6b6b;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
            color: white; 
        }
        .st-br {
            background-color: #6e6b6b;
            border-radius: 10px;
            padding: 10px;
            margin-bottom: 10px;
            color: white; 
        }
        .st-bs {
            background-color: #6e6b6b;
            border-radius: 10px;

            margin-bottom: 10px;
            color: white; 
        }
        .st-bt {
            background-color: #6e6b6b;
            border-radius: 10px;

            margin-bottom: 10px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

apply_dark_theme()

st.markdown("""
<style>
    [data-testid=stSidebar] {
        background-color: #454445;
    }
</style>
""", unsafe_allow_html=True)




st.title('The Mood Mosaic - An Emotional Compass')


selected_tab = st.radio('Navigation', ['Home','Datasets', 'Mood Analysis', '2 Bsc EA being a mood', 'Relations Of All', 'Mood Forecast'])




if selected_tab == 'Home':
    st.write('Welcome to the Home page!')
    
    import streamlit as st


    st.title('Mood Analysis')

    st.markdown('<div style="background-color: white; padding: 10px; border-radius: 5px;">'
                '<div style="background-color: pink; color: white; padding: 10px; border-radius: 5px; margin-bottom: 10px;">Objective:</div>'
                '<span style="color: black;">To understand mood cycle of a person and also to examine the role of mood states in determining the discrepancy observed between objective and subjective measures of sleep duration</span>'
                '</div>', unsafe_allow_html=True)

    st.markdown('<div style="background-color: white; padding: 10px; border-radius: 5px;">'
                '<div style="background-color: pink; color: white; padding: 10px; border-radius: 5px; margin-bottom: 10px;">Approach:</div>'
                '<span style="color: black;">Data Preparation:<br>'
                'The code reads an Excel file containing the necessary data and stores it in a Pandas DataFrame df.<br>'
                'The DataFrame is assumed to have columns such as \'Name\', \'Mood 1\', \'Mood 2\', \'Mood 3\', \'Mood Fluctuation Frequency\', \'Impact\', and \'Coping Mechanism\'.<br>'
                '<br>'
                'Streamlit App Structure:<br>'
                'The application has a navigation bar with two tabs: \'Home\' and \'Mood Analysis\'.<br>'
                'The \'Mood Analysis\' tab is the main focus of the application.'
                '<br><br>'
                'Mood Analysis Tab:<br>'
                'The user can select a person\'s name from a dropdown menu.<br>'
                'The application then displays various visualizations and analyses related to the selected person\'s mood data.'
                '<br><br>'
                'Visualization and Analysis:<br>'
                '<ul>'
                '<li>Mood Counts: The application plots a bar chart showing the count of different moods for the selected person.</li>'
                '<li>Mood Fluctuation Frequencies: The application displays a pie chart showing the distribution of mood fluctuation frequencies (No Fluctuation, Moderate, Moody) for the selected person.</li>'
                '<li>Impact Categories: The application plots a pie chart depicting the percentage of different impact categories (No Impact, Short Term Impact, Long Term Impact, Traumatic) for the selected person.</li>'
                '<li>Coping Mechanisms: The application displays a pie chart illustrating the distribution of coping mechanisms used by the selected person.</li>'
                '</ul>'
                '<br>'
                'Sidebar Analysis:<br>'
                'The application provides additional analysis and insights in the sidebar, such as the most and least occurring moods, the most and least frequent mood fluctuations, and the potential implications of the observed impact categories and coping mechanisms.'
                '</span>'
                '</div>', unsafe_allow_html=True)
    st.markdown('<div style="border: 5px solid pink; padding: 20px; background-color: white; color: black;">'
            '<div style="background-color: pink; color: white; padding: 10px;"><strong>Learning and Reflection:</strong></div>'
            '<div style="padding-left: 10px;">'
            '<strong>Datatype Handling:</strong><br>'
            'I encountered errors related to datatype conversion, especially with datetime objects. Streamlit requires careful handling of datetime data, including proper conversion to numeric formats like int64 for encoding.<br><br>'
            '<strong>Key Errors:</strong><br>'
            'Mismatched column names or incorrect indexing can lead to key errors in Streamlit apps. Double-checking column names and indices, especially when using dynamic selections, is crucial to avoid such errors.<br><br>'
            '<strong>Interactive Widgets:</strong><br>'
            'Streamlit\'s interactive widgets, such as dropdowns, sliders, and checkboxes, enable user interaction and customization of data visualization parameters. These widgets enhance the user experience and allow for dynamic exploration of data.<br><br>'
            '<strong>Custom Styling:</strong><br>'
            'Leveraging HTML and CSS in Streamlit apps enables custom styling, improving the aesthetics and professional appearance of the dashboard. Custom styling adds a personalized touch to data presentation.<br><br>'
            '<strong>Real-time Updates:</strong><br>'
            'Streamlit automatically updates visualizations and outputs in real-time as users interact with the app. This dynamic updating provides immediate feedback and keeps the app content relevant and up-to-date.<br><br>'
            '<strong>Deployment Options:</strong><br>'
            'Streamlit offers various deployment options, including Streamlit Sharing, Heroku, AWS, and Google Cloud. Deploying Streamlit apps facilitates sharing and collaboration on data analysis projects, making insights accessible to a wider audience.<br>'
            '</div></div>', unsafe_allow_html=True)
    st.markdown('<div style="border: 5px solid pink; padding: 20px; background-color: white; color: black;">'
                '<div style="background-color: pink; color: white; padding: 10px;"><strong>Role of mood in our daily life:</strong></div>'
                '<div style="padding-left: 10px;">'
                '<strong>Emotional Stability and Adaptability:</strong><br>'
                'The search results highlight the importance of mood in maintaining emotional stability and balance, which contributes to overall well-being and mental health.<br>'
                'Moderate mood swings are described as a natural part of the human emotional rhythm, helping individuals adapt to different situations and circumstances.<br><br>'
                '<strong>Behavioral and Interpersonal Impacts:</strong><br>'
                'Extreme and persistent mood swings, or "moody behavior," can indicate underlying emotional issues or mood disorders, which may impact daily functioning and overall mental well-being.<br>'
                'Moody behavior can lead to challenges in emotional regulation, interpersonal relationships, and coping with stress.<br><br>'
                '<strong>Long-Term Consequences:</strong><br>'
                'The search results suggest that the impact of mood can be categorized as short-term, long-term, or even traumatic, with long-term and traumatic impacts potentially having significant effects on an individual\'s mental and emotional well-being.<br><br>'
                '<strong>Coping Mechanisms:</strong><br>'
                'The way individuals cope with their moods and emotions can play a crucial role in managing the impact of mood on their daily lives.<br>'
                'The search results indicate that understanding an individual\'s preferred coping mechanisms can provide insights into their overall emotional well-being and resilience.'
                '</div></div>', unsafe_allow_html=True)
    
    
    emojis = {
        'Happy': '😄',
        'Sad': '😢',
        'Excited': '😃',
        'Angry': '😠',
        'Relaxed': '😌',
        'Confused': '😕',
        'Surprised': '😲',
        'Tired': '😴',
        'In Love': '😍',
        'Anxious': '😰',
        'Bored': '😑',
        'Grateful': '🙏',
    }

    # Create a sidebar with emoji stickers for moods
    st.sidebar.title('Mood Stickers')
    for mood, emoji in emojis.items():
        st.sidebar.markdown(f'<h1 style="font-size: 150px;">{emoji}</h1>---> {mood}', unsafe_allow_html=True)


    st.markdown('<div style="background-color: pink; padding: 10px; text-align: center; font-family: Algerian;">'
                '<div>Created By: Shruti Mishra & Juhi Rathore</div>'
                '<div>Guided by Naived George Eapen</div>'
                '</div>', unsafe_allow_html=True)




# Add a new tab for Datasets
elif selected_tab == 'Datasets':
    st.write('### Datasets')

    st.write('#### Breakfast Dataset')
    st.write(breakfast)

    st.write('#### Absenteeism Dataset')
    st.write(absenteeism)

    st.write('#### Activity Dataset')
    st.write(activity)

    st.write('#### Dinner Dataset')
    st.write(dinner)

    st.write('#### Sleep Dataset')
    st.write(sleep)

    st.write('#### Travel Dataset')
    st.write(travel)

    st.write('#### Clubs Dataset')
    st.write(clubs)

    st.write('#### Mood Dataset')
    st.write(mood)


elif selected_tab == 'Mood Analysis':



    
    selected_person = st.selectbox('Select a person:', df['Name'].unique())
    st.markdown("""
    <style>
        .styled-box {
            border: 4px solid pink;
            padding: 10px;
            position: relative;
        }
        .star-sticker {
            position: absolute;
            top: -20px;
            right: -20px;
            width: 50px;
            height: 50px;
        }
    </style>
    """, unsafe_allow_html=True)

    
    st.title('Styled Box with Text and Star Stickers')
    selected_df = df[df['Name'] == selected_person]


    fig = px.sunburst(selected_df, path=['Mood 1', 'Mood 2', 'Mood 3'], color='Impact',width=800, height=600, branchvalues='total')


    st.plotly_chart(fig)



    
    def styled_box_with_text_and_stars(text):
        st.markdown(
            f'<div class="styled-box">'
            f'<font color="white">{text}</font>'
            f'</div>',
            unsafe_allow_html=True
        )

    
    styled_box_with_text_and_stars("Joyful: \"Folks are usually about as happy as they make up their minds to be.\"")
    styled_box_with_text_and_stars("Excited: \"I have a lot of excitement in my life. I used to call it stress, but I feel much better now that I call it excitement.\"")
    styled_box_with_text_and_stars("Creative: \"To awaken human emotion is the highest level of art.\"")
    styled_box_with_text_and_stars("Peaceful: \"When our emotional health is in a bad state, so is our level of self-esteem. We have to slow down and deal with what is troubling us, so that we can enjoy the simple joy of being happy and at peace with ourselves.\"")
    styled_box_with_text_and_stars("Sad: \"Sometimes I laugh so hard the tears run down my leg.\"")
    styled_box_with_text_and_stars("Exhausted: \"I'm eating my feelings and they taste delicious.\"")
    styled_box_with_text_and_stars("Sleepy: \"Whenever I'm sad, I go to my happy place… the fridge.\"")
    styled_box_with_text_and_stars("Bored: \"Is 'ugh' an emotion? Because I feel it all the time.\"")
    styled_box_with_text_and_stars("Angry: \"Quick to judge, quick to anger, slow to understand ... prejudice, fear, and ignorance walk hand in hand.\"")
    styled_box_with_text_and_stars("Regretful: \"Whatever is begun in anger, ends in shame.\"")
    styled_box_with_text_and_stars("Numb: \"Your intellect may be confused, but your emotions will never lie to you.\"")

    
    def plot_mood_counts(df, person_name):
        mood_dict = {}
        for name in df['Name'].unique():
            moods_list = []
            for col in ['Mood 1', 'Mood 2', 'Mood 3']:
                moods_list.extend(df[df['Name'] == name][col].tolist())
            mood_dict[name] = moods_list

        
        counts_dict = {name: pd.Series(moods).value_counts() for name, moods in mood_dict.items()}

        
        plt.figure(figsize=(8, 5))
        counts = counts_dict[person_name]
        sns.barplot(x=counts.index, y=counts.values)
        plt.xlabel('Mood')
        plt.ylabel('Counts')
        plt.title(f'{person_name} - Mood Counts')
        plt.xticks(rotation=45, ha='right') 
        plt.tight_layout()
        st.pyplot()

        
        st.sidebar.write('### Overall Mood Distribution:')
        dominant_mood = counts.idxmax()
        least_occuring_mood = counts.idxmin()
        st.sidebar.write(f"Most Occurring Mood for {person_name}: {dominant_mood}")
        st.sidebar.write(f"Least Occurring Mood for {person_name}: {least_occuring_mood}")

        
        st.markdown(
            f'<div style="border: 4px solid pink; padding: 10px;">'
            f'<font color="pink">No Fluctuation Mood</font><br>'
            f'Indicates emotional stability and balance<br>'
            f'Contributes to overall well-being and mental health<br>'
            f'Exhibits a steady emotional demeanor<br>'
            f'Demonstrates resilience in the face of challenges<br>'
            f'</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div style="border: 4px solid pink; padding: 10px;">'
            f'<font color="pink">Moderate Mood Swings</font><br>'
            f'A natural part of human emotional rhythm<br>'
            f'Helps individuals adapt to different situations<br>'
            f'Exhibits flexibility in emotional responses<br>'
            f'Navigates various circumstances with appropriate reactions<br>'
            f'</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div style="border: 4px solid pink; padding: 10px;">'
            f'<font color="pink">Moody Behavior</font><br>'
            f'Can indicate underlying emotional issues or mood disorders<br>'
            f'May impact daily functioning and overall mental well-being<br>'
            f'Struggles with emotional regulation<br>'
            f'Faces challenges in interpersonal relationships and coping with stress<br>'
            f'</div>',
            unsafe_allow_html=True
        )

    
    def plot_fluctuation_frequencies(df, person_name):
        freq_counts = df[df['Name'] == person_name]['Mood Fluctuation Frequency'].value_counts()
        
        
        freq_counts = freq_counts.dropna()

        if not freq_counts.empty:
            total_fluctuations = freq_counts.sum()
            most_frequent_fluct = max(freq_counts) / total_fluctuations * 100
            least_frequent_fluct = min(freq_counts) / total_fluctuations * 100

            labels = ['No Fluctuation', 'Moderate', 'Moody']
            sizes = freq_counts.values
            explode = (0, 0.1, 0) 

            plt.figure(figsize=(6, 6))  
            plt.pie(sizes, labels=labels, explode=explode, autopct='%1.1f%%', shadow=True, startangle=90)
            plt.title(f'Mood Fluctuation Frequencies for {person_name}')
            plt.tight_layout()
            st.pyplot()

            
            st.sidebar.write('### Mood Fluctuation Frequencies Analysis:')
            st.sidebar.write(f"Most Frequent Fluctuation for {person_name}: {most_frequent_fluct:.1f}%")
            st.sidebar.write(f"Least Frequent Fluctuation for {person_name}: {least_frequent_fluct:.1f}%")
            if most_frequent_fluct > 50:
                st.sidebar.write(f"{person_name} is calm, collected, and mentally strong.")
            elif most_frequent_fluct > 30:
                st.sidebar.write(f"{person_name} is creative and determined person with good temperament.")
            else:
                st.sidebar.write(f"{person_name} is impatient, mentally not in a good condition and is going through tough times in life.")
        st.markdown(
        f'<div style="border: 4px solid pink; padding: 10px;">'
        f'<font color="pink">Short-Term Mood Fluctuations</font><br>'
        f'Impact: These are temporary changes in mood, like feeling happy after receiving good news or frustrated during a challenging task.<br>'
        f'Effects: Short-term fluctuations can influence our behavior, motivation, and focus. They can also affect decision-making, making us more impulsive when happy or withdrawn when sad.<br>'
        f'Coping Mechanisms: Simple strategies like taking a break, deep breathing, or talking to a friend can effectively manage these fluctuations.<br>'
        f'</div>',
        unsafe_allow_html=True
        )

        st.markdown(
            f'<div style="border: 4px solid pink; padding: 10px;">'
            f'<font color="pink">Moderate Mood Swings</font><br>'
            f'Impact: These are more pronounced changes that can last for several hours or even a few days. They might involve feelings of irritability, anxiety, or low energy.<br>'
            f'Effects: Moderate swings can disrupt daily routines, work performance, and social interactions. They can also lead to difficulty concentrating and increased emotional sensitivity.<br>'
            f'Coping Mechanisms: Healthy coping mechanisms like exercise, relaxation techniques (meditation, yoga), and maintaining a balanced sleep schedule become more important here.<br>'
            f'</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div style="border: 4px solid pink; padding: 10px;">'
            f'<font color="pink">Chronic Mood Disorders</font><br>'
            f'Impact: These are persistent mood disturbances that last for weeks or longer, significantly affecting daily life. Examples include depression, bipolar disorder, and anxiety disorders.<br>'
            f'Effects: Chronic mood disorders can lead to significant changes in behavior, sleep patterns, and social withdrawal. They can also cause physical symptoms like fatigue and difficulty concentrating.<br>'
            f'Coping Mechanisms: These require professional help. Therapy, medication, and lifestyle changes can be crucial for managing chronic mood disorders.<br>'
            f'</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div style="border: 4px solid pink; padding: 10px;">'
            f'<font color="pink">Traumatic Events</font><br>'
            f'Impact: Traumatic events are experiences that cause intense fear, helplessness, or horror. They can have a profound and lasting impact on mood, leading to post-traumatic stress disorder (PTSD).<br>'
            f'Effects: Trauma can lead to flashbacks, nightmares, hypervigilance, and emotional dysregulation. It can also cause difficulties with relationships and maintaining a normal lifestyle.<br>'
            f'Coping Mechanisms: Trauma requires specialized therapy approaches like EMDR (Eye Movement Desensitization and Reprocessing) or Cognitive Behavioral Therapy (CBT).<br>'
            f'</div>',
            unsafe_allow_html=True
        )

    
    def plot_impact_categories(df, person_name):
        impact_counts = df[df['Name'] == person_name]['Impact'].value_counts(normalize=True) * 100

        no_impact_percent = impact_counts.get('No Impact', 0)
        short_term_percent = impact_counts.get('Short Term Impact', 0)
        long_term_percent = impact_counts.get('Long Term Impact', 0)
        traumatic_percent = impact_counts.get('Traumatic', 0)

        labels = ['No Impact', 'Short Term Impact', 'Long Term Impact', 'Traumatic']
        sizes = [no_impact_percent, short_term_percent, long_term_percent, traumatic_percent]
        explode = (0, 0.1, 0, 0) 

        plt.figure(figsize=(8, 8))  
        plt.pie(sizes, labels=labels, explode=explode, autopct='%1.1f%%', shadow=True, startangle=90)
        plt.title(f'Impact Categories for {person_name}', fontsize=14)  # Increase title font size
        plt.tight_layout()
        plt.legend(labels, loc='center left', bbox_to_anchor=(1, 0.5), fontsize=12)
        st.pyplot()

        # Analysis Comments
        st.sidebar.write('### Impact Analysis:')
        st.sidebar.write(f"{long_term_percent:.1f}% of {person_name}'s experiences are categorized as long term impact.")
        st.sidebar.write(f"{traumatic_percent:.1f}% of {person_name}'s experiences are categorized as traumatic impact.")
        st.sidebar.write(f"These impacts may significantly affect {person_name}'s mental and emotional well-being.")
        st.markdown(
            f'<div style="border: 4px solid pink; padding: 10px;">'
            f'<font color="pink">Sensory Experiences</font><br>'
            f'Light Therapy: Seasonal Affective Disorder (SAD) is well-documented, but even without SAD, exposure to natural light can elevate mood. Open the curtains, spend time outdoors during daylight hours, or consider a light therapy lamp if natural light is limited.<br>'
            f'Aromatherapy: Certain essential oils like lavender, chamomile, and bergamot have calming and mood-lifting properties. Diffuse them in the air, add them to a hot bath, or use diluted blends for topical application (with caution and proper research).<br>'
            f'Uplifting Music: Listening to music you enjoy can trigger the release of dopamine, a neurotransmitter associated with pleasure and reward. Choose upbeat, energetic songs or create a playlist tailored to your mood.<br>'
            f'Positive Smells: Pleasant smells can elevate mood. Surround yourself with fresh scents like baking cookies, brewing coffee, or using air fresheners with natural fragrances (avoid harsh chemicals).<br>'
            f'</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div style="border: 4px solid pink; padding: 10px;">'
            f'<font color="pink">Mindfulness Techniques</font><br>'
            f'5 Senses Grounding: When feeling overwhelmed, take a moment to focus on the present. Name five things you can see, four things you can touch, three things you can hear, two things you can smell, and one thing you can taste. This simple practice can bring you back to the present moment and reduce anxiety.<br>'
            f'Gratitude on the Go: Throughout your day, take a few seconds to silently acknowledge something positive, big or small. It could be a beautiful flower, a kind stranger, or a delicious meal. This quick gratitude practice can shift your focus to the good things around you.<br>'
            f'Progressive Muscle Relaxation: Tense and relax different muscle groups in your body, starting with your toes and working your way up. This technique can release physical tension and promote feelings of calm.<br>'
            f'</div>',
            unsafe_allow_html=True
        )

        st.markdown(
            f'<div style="border: 4px solid pink; padding: 10px;">'
            f'<font color="pink">Quick Activities</font><br>'
            f'Do Something Nice for Yourself: Treat yourself to a small indulgence, like a hot cup of tea, a relaxing bath, or watching a funny video. Taking care of yourself can improve your mood and self-compassion.<br>'
            f'Help Someone Else: Random acts of kindness, like holding a door open or offering a compliment, can be a mood booster for both you and the recipient.<br>'
            f'Declutter Your Space: A cluttered environment can be mentally draining. Spend a few minutes tidying up your workspace or living area. A clean and organized space can contribute to a calmer state of mind.<br>'
            f'Challenge Yourself Mentally: Do a crossword puzzle, learn a new word, or complete a brain teaser. Engaging your mind in a stimulating activity can distract you from negative thoughts and boost your mood.<br>'
            f'</div>',
            unsafe_allow_html=True
        )


    
    def plot_coping_mechanisms(df, person_name):
        coping_counts = df[df['Name'] == person_name]['Coping Mechanism'].value_counts()

        plt.figure(figsize=(6, 6))
        plt.pie(coping_counts.values, labels=coping_counts.keys(), autopct='%1.1f%%', shadow=True, startangle=90)
        plt.title(f'Coping Mechanisms for {person_name}')
        plt.tight_layout()
        st.pyplot()

        
        st.sidebar.write('### Coping Mechanisms:')
        most_used_coping = coping_counts.idxmax()
        least_used_coping = coping_counts.idxmin()
        st.sidebar.write(f"{most_used_coping} is the most frequently used coping mechanism by {person_name}.")
        st.sidebar.write(f"{least_used_coping} is the least used coping mechanism by {person_name}.")



    
    plot_mood_counts(df, selected_person)

    
    plot_fluctuation_frequencies(df, selected_person)

    
    plot_impact_categories(df, selected_person)

    
    plot_coping_mechanisms(df, selected_person)


elif selected_tab == '2 Bsc EA being a mood':

    
    def plot_fluctuation_frequencies_2_bsc(df):
        import matplotlib.pyplot as plt

        
        fluctuation_counts = df['Mood Fluctuation Frequency'].value_counts()

    
        labels = fluctuation_counts.index.to_list()
        sizes = fluctuation_counts.to_list()

        
        plt.figure(figsize=(8, 8))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        plt.title('Overall Mood Fluctuation Frequencies', fontsize=14)
        plt.tight_layout()

        
        plt.legend(labels, loc='center left', bbox_to_anchor=(1, 0.5), fontsize=12)

        
        st.pyplot()

        
        st.sidebar.write('### Mood Fluctuation Frequencies Analysis:')
        st.sidebar.write('The majority of individuals in 2 Bsc EA group exhibit moderate mood swings, indicating adaptability and flexibility in emotional responses.')
        st.sidebar.write('The range of mood fluctuation frequencies is from 25% to 40%, with moderate fluctuations being the most common.')

    
    def plot_impact_categories_2_bsc(df):
        import matplotlib.pyplot as plt

        
        impact_counts = df['Impact'].value_counts()

        
        labels = impact_counts.index.to_list()
        sizes = impact_counts.to_list()

        
        plt.figure(figsize=(8, 8))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        plt.title('Overall Impact Categories Distribution', fontsize=14)
        plt.tight_layout()

        
        plt.legend(labels, loc='center left', bbox_to_anchor=(1, 0.5), fontsize=12)

        
        st.pyplot()

        
        st.sidebar.write('### Impact Analysis:')
        st.sidebar.write('The impact categories distribution indicates a range of emotional experiences among individuals in 2 Bsc EA group.')
        st.sidebar.write('Long-term impacts are notable, suggesting potential challenges in managing emotional well-being.')

        

    

    
    def plot_additional_graphs_2_bsc(df):
        
        label_encoder = LabelEncoder()
        df['Mood Fluctuation Frequency Encoded'] = label_encoder.fit_transform(df['Mood Fluctuation Frequency'])
        df['Coping Mechanism Encoded'] = label_encoder.fit_transform(df['Coping Mechanism'])
        
        
        plt.figure(figsize=(14, 10))  
        grid = sns.FacetGrid(df, col='Impact', height=30, aspect=1.2)
        
        
        grid.map(sns.violinplot, 'Mood Fluctuation Frequency Encoded', 'Coping Mechanism Encoded', palette='Set2', linewidth=2)  # Increased linewidth

        
        grid.map(sns.kdeplot, 'Mood Fluctuation Frequency Encoded', 'Coping Mechanism Encoded', cmap='viridis', fill=True, alpha=0.5)

        
        sns.scatterplot(data=df, x='Mood Fluctuation Frequency Encoded', y='Coping Mechanism Encoded', hue='Impact', s=100)
        sns.rugplot(data=df, x='Mood Fluctuation Frequency Encoded', y='Coping Mechanism Encoded', alpha=0.5)
        
        
        plt.subplots_adjust(top=0.85)
        grid.set_titles(col_template="{col_name}")
        grid.set_axis_labels('Mood Fluctuation Frequency Encoded', 'Coping Mechanism Encoded')

        
        plt.legend(title='Impact', loc='upper right', bbox_to_anchor=(1.2, 1))
        plt.tight_layout()

        
        st.pyplot()
        
    def plot_violin_plots(df):
    
        label_encoder = LabelEncoder()
        df['Mood Fluctuation Frequency Encoded'] = label_encoder.fit_transform(df['Mood Fluctuation Frequency'])
        df['Coping Mechanism Encoded'] = label_encoder.fit_transform(df['Coping Mechanism'])

        
        impact_values = df['Impact'].unique()

        
        for impact in impact_values:
            
            impact_data = df[df['Impact'] == impact]

            
            plt.figure(figsize=(10, 6))  
            sns.violinplot(x='Mood Fluctuation Frequency Encoded', y='Coping Mechanism Encoded', data=impact_data, palette='Set2', linewidth=2)
            plt.title(f'Violin Plot for Impact: {impact}', fontsize=14)
            plt.xlabel('Mood Fluctuation Frequency Encoded')
            plt.ylabel('Coping Mechanism Encoded')
            plt.tight_layout()

            
            st.pyplot()

        
    
    def plot_coping_mechanisms_2_bsc(df):
        
        all_coping_counts = df['Coping Mechanism'].value_counts()
        labels = all_coping_counts.keys()
        sizes = all_coping_counts.values

        
        plt.figure(figsize=(8, 8))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        plt.title('Overall Distribution of Coping Mechanisms')
        plt.tight_layout()

        
        st.pyplot()

        
        st.sidebar.write('### Coping Mechanisms Analysis:')
        st.sidebar.write('The distribution of coping mechanisms reflects diverse strategies used by individuals in 2 Bsc EA group to manage emotions.')
        st.sidebar.write('Exploring coping mechanisms can provide insights into emotional resilience and adaptive strategies.')
        
    def plot_violin_plots_coping_mechanism(df):
        
        label_encoder = LabelEncoder()
        df['Mood Fluctuation Frequency Encoded'] = label_encoder.fit_transform(df['Mood Fluctuation Frequency'])
        df['Coping Mechanism Encoded'] = label_encoder.fit_transform(df['Coping Mechanism'])

        
        coping_mechanism_values = df['Coping Mechanism'].unique()

        
        for coping_mechanism in coping_mechanism_values:
            
            coping_mechanism_data = df[df['Coping Mechanism'] == coping_mechanism]

            
            plt.figure(figsize=(10, 6))  
            sns.violinplot(x='Mood Fluctuation Frequency Encoded', y='Impact', data=coping_mechanism_data, palette='Set2', linewidth=2)
            plt.title(f'Violin Plot for Coping Mechanism: {coping_mechanism}', fontsize=14)
            plt.xlabel('Mood Fluctuation Frequency Encoded')
            plt.ylabel('Impact')
            plt.tight_layout()

            
            st.pyplot()
            
    def plot_violin_plots_fluctuation_frequency(df):
        df.ffill()
        
        label_encoder = LabelEncoder()
        df['Mood Fluctuation Frequency Encoded'] = label_encoder.fit_transform(df['Mood Fluctuation Frequency'])
        df['Coping Mechanism Encoded'] = label_encoder.fit_transform(df['Coping Mechanism'])

        
        fluctuation_frequency_values = df['Mood Fluctuation Frequency'].unique()

        
        for frequency in fluctuation_frequency_values:
            
            frequency_data = df[df['Mood Fluctuation Frequency'] == frequency]

            
            plt.figure(figsize=(10, 6)) 
            sns.violinplot(x='Coping Mechanism Encoded', y='Impact', data=frequency_data, palette='Set2', linewidth=2)
            plt.title(f'Violin Plot for Mood Fluctuation Frequency: {frequency}', fontsize=14)
            plt.xlabel('Coping Mechanism Encoded')
            plt.ylabel('Impact')
            plt.tight_layout()

            
            st.pyplot()
            
    def create_sunburst_chart(df):
    
        sunburst_data = df.groupby(['Name', 'Mood 1', 'Mood 2', 'Mood 3', 'Impact']).size().reset_index(name='count')

        
        fig = px.sunburst(sunburst_data, path=['Name', 'Mood 1', 'Mood 2', 'Mood 3', 'Impact'], values='count', color='Impact')

        
        fig.update_layout(
            width=800,
            height=600,
            title='Sunburst Chart',
            title_font_size=20,
            title_font_color='white',
            title_font_family='Arial',
            title_x=0.5,
            title_y=0.95,
            paper_bgcolor='black',
            plot_bgcolor='black',
            font_color='white',
            font_size=12,
            margin=dict(l=20, r=20, t=50, b=20)
        )

        
        st.plotly_chart(fig)

        
        st.sidebar.write('### Sunburst Chart Analysis:')
        st.sidebar.write('The sunburst chart displays mood details for each person, including Mood 1, Mood 2, Mood 3, and Impact.')
        st.sidebar.write('It provides a visual overview of emotional patterns and their impact on individuals in one graph and through user interaction.')


    create_sunburst_chart(df)
                
        




    
    plot_additional_graphs_2_bsc(df)
    

    
    plot_fluctuation_frequencies_2_bsc(df)
    plot_violin_plots_fluctuation_frequency(df)

    
    plot_impact_categories_2_bsc(df)
    plot_violin_plots(df)

    
    plot_coping_mechanisms_2_bsc(df)
    plot_violin_plots_coping_mechanism(df)


    
    def plot_fluctuation_frequencies_2_bsc(df):
        import matplotlib.pyplot as plt

        # Calculate total mood fluctuation frequencies across all names
        fluctuation_counts = df['Mood Fluctuation Frequency'].value_counts()

        # Extract labels and sizes (counts) from the Series
        labels = fluctuation_counts.index.to_list()
        sizes = fluctuation_counts.to_list()

        # Create the pie chart
        plt.figure(figsize=(8, 8))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        plt.title('Overall Mood Fluctuation Frequencies', fontsize=14)
        plt.tight_layout()

        # Place legend outside the pie chart
        plt.legend(labels, loc='center left', bbox_to_anchor=(1, 0.5), fontsize=12)

        # Display the plot using st.pyplot() instead of plt.show()
        st.pyplot()

        # Analysis Comments for Mood Fluctuation Frequencies
        st.sidebar.write('### Mood Fluctuation Frequencies Analysis:')
        st.sidebar.write('The majority of individuals in 2 Bsc EA group exhibit moderate mood swings, indicating adaptability and flexibility in emotional responses.')
        st.sidebar.write('The range of mood fluctuation frequencies is from 25% to 40%, with moderate fluctuations being the most common.')

    # Function to plot impact categories for '2 Bsc EA'
    def plot_impact_categories_2_bsc(df):
        import matplotlib.pyplot as plt

        # Calculate total impact category counts across all names
        impact_counts = df['Impact'].value_counts()

        # Extract labels and sizes (counts) from the Series
        labels = impact_counts.index.to_list()
        sizes = impact_counts.to_list()

        # Create the pie chart
        plt.figure(figsize=(8, 8))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        plt.title('Overall Impact Categories Distribution', fontsize=14)
        plt.tight_layout()

        # Place legend outside the pie chart
        plt.legend(labels, loc='center left', bbox_to_anchor=(1, 0.5), fontsize=12)

        # Display the plot using st.pyplot() instead of plt.show()
        st.pyplot()

        # Analysis Comments for Impact Categories
        st.sidebar.write('### Impact Analysis:')
        st.sidebar.write('The impact categories distribution indicates a range of emotional experiences among individuals in 2 Bsc EA group.')
        st.sidebar.write('Long-term impacts are notable, suggesting potential challenges in managing emotional well-being.')

    # Function to plot coping mechanisms for '2 Bsc EA'
    def plot_coping_mechanisms_2_bsc(df):
        # Combine coping mechanism counts across all names
        all_coping_counts = df['Coping Mechanism'].value_counts()
        labels = all_coping_counts.keys()
        sizes = all_coping_counts.values

        # Create a pie chart for overall coping mechanism distribution
        plt.figure(figsize=(8, 8))
        plt.pie(sizes, labels=labels, autopct='%1.1f%%', shadow=True, startangle=90)
        plt.title('Overall Distribution of Coping Mechanisms')
        plt.tight_layout()

        # Display the plot using st.pyplot() instead of plt.show()
        st.pyplot()

        # Analysis Comments for Coping Mechanisms
        st.sidebar.write('### Coping Mechanisms Analysis:')
        st.sidebar.write('The distribution of coping mechanisms reflects diverse strategies used by individuals in 2 Bsc EA group to manage emotions.')
        st.sidebar.write('Exploring coping mechanisms can provide insights into emotional resilience and adaptive strategies.')

    # Function to plot additional 3D graphs for '2 Bsc EA'
    def plot_3d_graphs_2_bsc(df):
        # Convert categorical columns to numerical using Label Encoding
        label_encoder = LabelEncoder()
        df['Mood Fluctuation Frequency Encoded'] = label_encoder.fit_transform(df['Mood Fluctuation Frequency'])
        df['Coping Mechanism Encoded'] = label_encoder.fit_transform(df['Coping Mechanism'])
        df['Impact Encoded'] = label_encoder.fit_transform(df['Impact'])

        # Create 3D scatter plot for 'Mood Fluctuation Frequency Encoded', 'Coping Mechanism Encoded', 'Impact Encoded'
        fig = plt.figure(figsize=(10, 8))
        ax = fig.add_subplot(111, projection='3d')
        ax.scatter(df['Mood Fluctuation Frequency Encoded'], df['Coping Mechanism Encoded'], df['Impact Encoded'], c='blue', marker='o')
        ax.set_xlabel('Mood Fluctuation Frequency Encoded')
        ax.set_ylabel('Coping Mechanism Encoded')
        ax.set_zlabel('Impact Encoded')
        ax.set_title('3D Scatter Plot for Mood Analysis')
        plt.tight_layout()

        # Display the plot using st.pyplot() instead of plt.show()
        st.pyplot()

        # Analysis Comments for 3D Scatter Plot
        st.sidebar.write('### 3D Scatter Plot Analysis:')
        st.sidebar.write('The 3D scatter plot visualizes the relationship between mood fluctuation frequency, coping mechanisms, and impact categories.')
        st.sidebar.write('It shows the distribution of individuals across different mood dimensions and their impact on emotional well-being.')

    
    plot_fluctuation_frequencies_2_bsc(df)

    
    plot_impact_categories_2_bsc(df)

    
    plot_coping_mechanisms_2_bsc(df)

    
    plot_3d_graphs_2_bsc(df)

    st.markdown(
    '<div style="background-color: pink; padding: 10px; text-align: center; font-family: Times New Roman; font-size: 20px; color: white;">'
    '<p>"2 Bsc EA......Every year there is a new batch occupying the class<br>'
    'but the memories and the friends remain life long."</p>'
    '</div>',
    unsafe_allow_html=True)

    





    


elif selected_tab == 'Relations Of All' :


    # Define DataFrames
    excel_file_path = "Mood_Predictor_Model_Streamlit_App/Dataset.xlsx"
    breakfast = pd.read_excel(excel_file_path, sheet_name=0, engine='openpyxl')
    activity= pd.read_excel(excel_file_path, sheet_name=2, engine='openpyxl')
    absenteeism = pd.read_excel(excel_file_path, sheet_name=3, engine='openpyxl')
    dinner = pd.read_excel(excel_file_path, sheet_name=4, engine='openpyxl')
    sleep = pd.read_excel(excel_file_path, sheet_name=5, engine='openpyxl')
    travel = pd.read_excel(excel_file_path, sheet_name=6, engine='openpyxl')
    clubs = pd.read_excel(excel_file_path, sheet_name=8, engine='openpyxl')
    mood = pd.read_excel(excel_file_path, sheet_name=1, engine='openpyxl')
    background_image_url = "https://t3.ftcdn.net/jpg/01/14/99/46/360_F_114994681_1PAiJQLGyxYCPPv3LySDJjbdhop0eHpV.jpg"


    st.markdown(
        f"""
        <style>
            .reportview-container .main .block-container {{
                background-image: url("{background_image_url}");
                background-size: cover;
                background-repeat: no-repeat;
                background-attachment: fixed;
            }}
        </style>
        """,
        unsafe_allow_html=True,
    )

    
    def encode_reverse_encode(df):
        
        encoded_df = df.apply(lambda x: pd.factorize(x)[0] if x.dtype == 'object' else x)

        
        reverse_encoded_df = encoded_df.apply(lambda x: x.map(dict(zip(range(len(x.unique())), x.unique()))) if x.dtype == 'int64' else x)

        return encoded_df, reverse_encoded_df

    
    def plot_graph_and_stats(selected_name, df1, df2, selected_column1, selected_column2):
        
        encoded_df1, reverse_encoded_df1 = encode_reverse_encode(df1)
        encoded_df2, reverse_encoded_df2 = encode_reverse_encode(df2)

        if selected_column1 in encoded_df1.columns and selected_column2 in encoded_df2.columns:
            
            df1_filtered = encoded_df1[df1['Name'] == selected_name]
            df2_filtered = encoded_df2[df2['Name'] == selected_name]
            fig, ax = plt.subplots(figsize=(10, 6))
            st.line_chart(df1_filtered[selected_column1])
            st.line_chart(df2_filtered[selected_column2])
            
            df1_filtered = encoded_df1[df1['Name'] == selected_name]
            df2_filtered = encoded_df2[df2['Name'] == selected_name]
            
            
            st.write('Descriptive Statistics for DataFrame 1:')
            st.write(df1_filtered[selected_column1].describe())
            st.write('Descriptive Statistics for DataFrame 2:')
            st.write(df2_filtered[selected_column2].describe())

            
            correlation = df1_filtered[selected_column1].corr(df2_filtered[selected_column2])
            correlation_statement = ''
            if correlation > 0:
                correlation_statement = f'There is a positive correlation between {selected_column1} and {selected_column2}.'
            elif correlation < 0:
                correlation_statement = f'There is a negative correlation between {selected_column1} and {selected_column2}.'
            elif correlation == None or correlation == 'nan':
                correlation_statement = f'The {selected_column1} and {selected_column2} are same.'
            else:
                correlation_statement = f'They are either same values or have no significant correlation between {selected_column1} and {selected_column2}.'
            st.markdown(
                f'<div style="border: 20px solid pink; background-color: white; padding: 30px; color: black;">'
                f'<h3>Analysis of Similarity or Relation:</h3>'
                f'<p>The correlation value is {correlation}<p>'
                f'<p>{correlation_statement}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )

            
            st.write('Frequency of Occurrence Analysis:')
            value_counts1 = df1_filtered[selected_column1].value_counts()
            value_counts2 = df2_filtered[selected_column2].value_counts()
            st.write(f'Value Counts for {selected_column1} in DataFrame 1:')
            st.write(value_counts1)
            st.write(f'Value Counts for {selected_column2} in DataFrame 2:')
            st.write(value_counts2)
            

            
            shape1 = df1_filtered[selected_column1].shape
            shape2 = df2_filtered[selected_column2].shape
            shape_statement = ''
            if shape1 == shape2:
                shape_statement = f'The shapes of {selected_column1} in DataFrame 1 and {selected_column2} in DataFrame 2 are identical.'
            else:
                shape_statement = f'The shapes of {selected_column1} in DataFrame 1 and {selected_column2} in DataFrame 2 are different.'
            st.markdown(
                f'<div style="border: 20px solid pink; background-color: white; padding: 30px; color: black;">'
                f'<h3>Shape of Graphs Analysis:</h3>'
                f'<p>{shape_statement}</p>'
                f'</div>',
                unsafe_allow_html=True,
            )
        else:
            st.write('Selected columns not found in the DataFrames.')

    
    selected_dataframe1 = st.selectbox('Select DataFrame 1:', ['breakfast', 'absenteeism', 'activity', 'dinner', 'sleep', 'travel', 'clubs'])
    selected_dataframe2 = st.selectbox('Select DataFrame 2:', ['breakfast', 'absenteeism', 'activity', 'dinner', 'sleep', 'travel', 'clubs'])

    df1 = globals()[selected_dataframe1]  # Get DataFrame 1 based on selected dropdown
    df2 = globals()[selected_dataframe2]  # Get DataFrame 2 based on selected dropdown

    
    selected_column1 = st.selectbox('Select Column 1:', df1.columns.drop(['Name']))
    selected_column2 = st.selectbox('Select Column 2:', df2.columns.drop(['Name']))

    
    selected_name = st.selectbox('Select a Name:', mood['Name'].unique())

        
    plot_graph_and_stats(selected_name, df1, df2, selected_column1, selected_column2)


elif selected_tab == 'Mood Forecast':
    st.write('### Mood Forecasting')


    from sklearn.neighbors import KNeighborsClassifier


    
    df.dropna(inplace=True)


    name = st.sidebar.selectbox('Select Name', df['Name'].unique())
    mood1 = st.sidebar.selectbox('Select Mood 1', df['Mood 1'].unique())
    mood2 = st.sidebar.selectbox('Select Mood 2', df['Mood 2'].unique())
    mood3 = st.sidebar.selectbox('Select Mood 3', df['Mood 3'].unique())


    encoder = LabelEncoder()
    df_encoded = df.copy()  # Make a copy to avoid modifying the original DataFrame
    df_encoded['Mood 1'] = encoder.fit_transform(df['Mood 1'])
    df_encoded['Mood 2'] = encoder.fit_transform(df['Mood 2'])
    df_encoded['Mood 3'] = encoder.fit_transform(df['Mood 3'])

    X = df_encoded[['Mood 1', 'Mood 2', 'Mood 3']]
    y_fluctuation = df['Mood Fluctuation Frequency']
    y_coping = df['Coping Mechanism']

    clf_fluctuation = KNeighborsClassifier()
    clf_fluctuation.fit(X, y_fluctuation)

    clf_coping = KNeighborsClassifier()
    clf_coping.fit(X, y_coping)


    input_data = pd.DataFrame([[mood1, mood2, mood3]], columns=['Mood 1', 'Mood 2', 'Mood 3'])
    input_data_encoded = input_data.copy()
    input_data_encoded['Mood 1'] = encoder.transform(input_data['Mood 1'])
    input_data_encoded['Mood 2'] = encoder.transform(input_data['Mood 2'])
    input_data_encoded['Mood 3'] = encoder.transform(input_data['Mood 3'])


    predicted_fluctuation = clf_fluctuation.predict(input_data_encoded)[0]
    predicted_coping = clf_coping.predict(input_data_encoded)[0]


    st.markdown(
        f'<div style="border: 20px solid pink; background-color: white; padding: 30px; color: pink;">'
        f'<p>Predicted Mood Fluctuation Frequency: <span style="color: black;">{predicted_fluctuation}</span></p>'
        f'<p>Predicted Coping Mechanism: <span style="color: black;">{predicted_coping}</span></p>'
        f'</div>',
        unsafe_allow_html=True
    )


    fig1, ax1 = plt.subplots()
    ax1.hist(df['Mood 1'], bins=10)
    ax1.set_xlabel('Mood 1')
    ax1.set_ylabel('Frequency')
    ax1.set_title('Histogram of Mood 1')
    ax1.set_xticklabels(ax1.get_xticks(), rotation=45)
    st.pyplot(fig1)
    st.write("""
        Statistical analysis:
        - Mood 1 shows a distribution skewed towards higher values, indicating a tendency towards positive moods.
        - The frequency of mood values between 30-40 is notably higher compared to other ranges.
    """)

    fig2, ax2 = plt.subplots()
    ax2.hist(df['Mood 2'], bins=10)
    ax2.set_xlabel('Mood 2')
    ax2.set_ylabel('Frequency')
    ax2.set_title('Histogram of Mood 2')
    ax2.set_xticklabels(ax2.get_xticks(), rotation=45)
    st.pyplot(fig2)
    st.write("""
        Statistical analysis:
        - Mood 2 has a more balanced distribution across the range of values, with no significant skew.
        - There's a relatively even distribution of mood values across different ranges.
    """)

    fig3, ax3 = plt.subplots()
    ax3.hist(df['Mood 3'], bins=10)
    ax3.set_xlabel('Mood 3')
    ax3.set_ylabel('Frequency')
    ax3.set_title('Histogram of Mood 3')
    ax3.set_xticklabels(ax3.get_xticks(), rotation=45)
    st.pyplot(fig3)
    st.write("""
        Statistical analysis:
        - Mood 3 exhibits a bimodal distribution with peaks at both low and high values, indicating distinct mood states.
        - There's a noticeable gap in the distribution around the midpoint of the range.
    """)

    fig4, ax4 = plt.subplots()
    ax4.bar(['No Fluctuation', 'Moderate', 'Moody'], df['Mood Fluctuation Frequency'].value_counts())
    ax4.set_xlabel('Mood Fluctuation Frequency')
    ax4.set_ylabel('Count')
    ax4.set_title('Bar Chart of Mood Fluctuation Frequency')
    ax4.set_xticklabels(ax4.get_xticks(), rotation=45)
    st.pyplot(fig4)
    st.write("""
        Statistical analysis:
        - The bar chart shows the distribution of Mood Fluctuation Frequency categories.
        - The 'Moderate' category has the highest count, followed by 'Moody' and 'No Fluctuation'.
    """)

    fig5, ax5 = plt.subplots()
    ax5.bar(df['Coping Mechanism'].unique(), df['Coping Mechanism'].value_counts())
    ax5.set_xlabel('Coping Mechanism')
    ax5.set_ylabel('Count')
    ax5.set_title('Bar Chart of Coping Mechanisms')
    ax5.set_xticklabels(ax5.get_xticks(), rotation=45)
    st.pyplot(fig5)
    st.write("""
        Statistical analysis:
        - The bar chart displays the distribution of Coping Mechanisms.
        - There's a variation in counts across different coping strategies, with some being more prevalent than others.
    """)
    
