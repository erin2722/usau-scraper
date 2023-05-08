from teamScraper import getTeamSchedule
import json

if __name__ == "__main__":
    # TODO: print documentation if this is called
    print("welcome to the usau_scraper")

    print(
        json.dumps(
            getTeamSchedule(
                schoolName='Columbia',
                teamName='Baewatch',
                genderDivision='Women',
                state='NY',
                competitionLevel='College',
                competitionDivision='Division 1',
                teamDesignation='B',
            ),
            indent=4,
        )
    )
