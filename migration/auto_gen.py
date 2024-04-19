import random
import datetime
from models import News

titles = [
    'Stunning Performance', 'Unbelievable Game', 'Historic Night', 'Incredible Showdown', 'Epic Battle',
    'Dramatic Finish', 'Spectacular Display', 'Memorable Matchup', 'Thrilling Encounter', 'Remarkable Achievement',
    'Game-Changing Moment', 'Unforgettable Victory', 'Heart-Stopping Play', 'Masterful Strategy', 'Dominant Display',
    'Unstoppable Force', 'Breathtaking Skill', 'Record-Breaking Performance', 'Legendary Game', 'Nail-Biting Finish',
    'Rising Star Shines', 'Veteran Leadership', 'Defensive Masterclass', 'Offensive Explosion', 'Clutch Performance',
    'Rookie Sensation', 'Comeback Victory', 'Upset Alert', 'Overtime Thriller', 'Statement Win',
    'Powerhouse Clash', 'Underdog Triumph', 'Revenge Game', 'Breakout Performance', 'Milestone Achievement',
    'Rivalry Renewed', 'Winning Streak Continues', 'Shock and Awe', 'Showdown of the Titans', 'Battle for Supremacy',
    # Add more titles here
]

teams = [
    'Atlanta Hawks', 'Boston Celtics', 'Brooklyn Nets', 'Charlotte Hornets', 'Chicago Bulls',
    'Cleveland Cavaliers', 'Dallas Mavericks', 'Denver Nuggets', 'Detroit Pistons', 'Golden State Warriors',
    'Houston Rockets', 'Indiana Pacers', 'Los Angeles Clippers', 'Los Angeles Lakers', 'Memphis Grizzlies',
    'Miami Heat', 'Milwaukee Bucks', 'Minnesota Timberwolves', 'New Orleans Pelicans', 'New York Knicks',
    'Oklahoma City Thunder', 'Orlando Magic', 'Philadelphia 76ers', 'Phoenix Suns', 'Portland Trail Blazers',
    'Sacramento Kings', 'San Antonio Spurs', 'Toronto Raptors', 'Utah Jazz', 'Washington Wizards'
]

# Sample players from each team
players = [
    'Trae Young', 'Jayson Tatum', 'Kevin Durant', 'LaMelo Ball', 'Zach LaVine',
    'Darius Garland', 'Luka Dončić', 'Nikola Jokić', 'Cade Cunningham', 'Stephen Curry',
    'Jalen Green', 'Tyrese Haliburton', 'Paul George', 'LeBron James', 'Ja Morant',
    'Jimmy Butler', 'Giannis Antetokounmpo', 'Anthony Edwards', 'Zion Williamson', 'RJ Barrett',
    'Shai Gilgeous-Alexander', 'Paolo Banchero', 'Joel Embiid', 'Devin Booker', 'Damian Lillard',
    'DeAaron Fox', 'Keldon Johnson', 'Pascal Siakam', 'Donovan Mitchell', 'Bradley Beal'
]

# Sample actions (you can add more to reach 100)
actions = [
    'scored a triple-double', 'hit the game-winning shot', 'dominated with 30 points and 15 rebounds',
    'led the team to victory', 'had an outstanding performance', 'made a crucial block in the final seconds',
    'scored a career-high 50 points', 'was unstoppable from beyond the arc', 'dished out 12 assists',
    'grabbed a season-high 20 rebounds', 'put on a defensive clinic', 'had a double-double with points and assists',
    'was a force in the paint', 'hit a buzzer-beater to win the game', 'had a perfect shooting night',
    'set a new record for three-pointers in a game', 'was named player of the game', 'made a game-changing steal',
    'had a monster dunk that energized the crowd', 'scored in double figures for the 10th straight game',
    'led a fourth-quarter comeback', 'had a clutch performance in overtime', 'was ejected after a heated argument',
    'suffered an injury and had to leave the game', 'was on fire, scoring 25 points in the first half',
    'broke the franchise record for assists', 'was a key player in a defensive showdown',
    'had a career night from the free-throw line',
    'achieved a new season-best in rebounds', 'was unstoppable, scoring in every quarter',
    'played a pivotal role in a major upset',
    'had a standout performance in a playoff game', 'was selected for the All-Star team',
    'made a significant contribution off the bench',
    'set a new personal best in blocks', 'led all scorers in a high-scoring affair',
    'was the top rebounder in a tough matchup',
    'showcased his skills with a triple-double', 'played a crucial role in breaking the teams losing streak',
    'was the driving force behind a winning streak',
    'made headlines with a controversial play', 'was praised for his sportsmanship',
    'faced criticism for a poor shooting night', 'bounced back with a strong performance after a slump',
    'was honored with a season award',
    'made a dramatic return from injury', 'was a key defender in a close game',
    'excelled in his role as a team leader',
    'demonstrated his versatility with multiple position plays',
    'was the highlight of the week with a spectacular move',
    'faced a tough challenge against a top defender', 'was recognized for his contribution to the community',
    'had a record-breaking night from the field',
    'showed off his athleticism with an impressive dunk', 'was the subject of trade rumors',
    'signed a lucrative contract extension',
    'was at the center of a coaching controversy', 'played a memorable final game before retirement',
    'was involved in a dramatic overtime thriller',
    'was a standout in the international competition', 'was instrumental in a historic team victory',
    'received a standing ovation for his performance',
    'was sidelined due to a suspension', 'made a significant impact in his rookie season',
    'was part of a blockbuster trade',
    'faced off against his former team', 'was honored with a jersey retirement ceremony',
    'set a new league record for consecutive free throws',
    'was a key factor in a defensive battle', 'showed resilience in a comeback win',
    'was the talk of the town with a controversial decision',
    'played with great intensity in a rivalry game', 'was the focus of an inspiring comeback story',
    'made a significant impact in the community outreach program',
    'was at the forefront of a major team announcement', 'played an unforgettable game in the finals',
    'was recognized for his outstanding leadership',
    'left a lasting legacy with his career achievements', 'was a central figure in a dramatic playoff series',
    'inspired fans with his dedication and work ethic',
    'was a major draw for the teams home games', 'played a key role in a historic season',
    'was a fan favorite for his entertaining play style',
    'was a mentor to younger players on the team', 'faced adversity with courage and determination',
    'was celebrated for his long-standing career',
    'made a surprise appearance in a charity event', 'was a dominant force in the paint',
    'showed exceptional skill in a showcase game',
    'was a key contributor in a team milestone', 'left an indelible mark on the game with his performance'
]


def generate_news():
    team = random.choice(teams)
    player = random.choice(players)
    action = random.choice(actions)
    title = random.choice(titles) + " for " + player

    # Define a date range for the random date
    start_date = datetime.date(2020, 10, 1)  # Start of the NBA season
    end_date = datetime.date(2023, 4, 1)     # End of the NBA season
    date = generate_random_date(start_date, end_date)
    content = f"On {date}, {player} of the {team} {action}."

    news = News(title=title, content=content, created_date=date)
    return news

def generate_random_date(start_date, end_date):
    """Generate a random date between start_date and end_date."""
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)
    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return random_date.strftime('%B %d, %Y')  # Format the date as Month day, Year