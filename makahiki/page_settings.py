PAGE_SETTINGS = {
    # actions page
    "actions" : 
        { "PAGE_TITLE" : "Actions",
          "BASE_TEMPLATE" : "logged_in_base.html",
          "LAYOUTS" :
              {"DEFAULT" :
                 (
                  (("upcoming_events", "40%"), ("smartgrid", "60%"),("scoreboard", "40%"),),
                 ),
               "PHONE_PORTRAIT" :
                 (("upcoming_events", "100%"),
                  ("smartgrid", "100%"),
                  ("scoreboard", "100%"),
                 ),
              },
        },

    # profile page
    "profile" :
        { "PAGE_TITLE" : "Profile",
          "BASE_TEMPLATE" : "logged_in_base.html",
          "LAYOUTS" :
              { "DEFAULT" :
                (
                  ("profile", "100%"),
                ),
                "PHONE_PORTRAIT" :
                (
                  ("profile", "100%"),
                ),
              },
        },

    # news page
    "news" :
        { "PAGE_TITLE" : "News",
          "BASE_TEMPLATE" : "logged_in_base.html",
          "LAYOUTS" :
              { "DEFAULT" :
                (
                  ("news", "100%"),
                ),
                "PHONE_PORTRAIT" :
                (
                  ("news", "100%"),
                ),
              },
        },

    # help page
    "help" :
        { "PAGE_TITLE" : "Help",
          "BASE_TEMPLATE" : "logged_in_base.html",
          "LAYOUTS" :
              { "DEFAULT" :
                (
                  ("help", "100%"),
                ),
                "PHONE_PORTRAIT" :
                (
                  ("help", "100%"),
                ),
              },
        },

    # energy page
    "energy" :
        { "PAGE_TITLE" : "Energy",
          "BASE_TEMPLATE" : "logged_in_base.html",
          "LAYOUTS" :
              { "DEFAULT" :
                (
                  ("energy", "100%"),
                ),
                "PHONE_PORTRAIT" :
                (
                  ("energy", "100%"),
                ),
              },
        },

    # prizes page
    "prizes" :
        { "PAGE_TITLE" : "Prizes",
          "BASE_TEMPLATE" : "logged_in_base.html",
          "LAYOUTS" :
              { "DEFAULT" :
                (
                  ("prizes", "100%"),
                ),
                "PHONE_PORTRAIT" :
                (
                  ("prizes", "100%"),
                ),
              },
        },

}