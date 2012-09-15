SRS
===

Spaced Repitition


features:

    high:
        make a way to display cards
        make a way to create decks
        make a way to add card to deck
        algorithm for SRS
        make user profile (I think we should get some social crap going on)
            name
            what decks
    low:
        get media working in card slots... use filepicker.io
        implement a template card system, for now it's just a front-back traditional card 
        user settings
        a "what the hell is SRS?!" page
        public deck repo
        

general site outline:

    /login.html - you login or register
    /register.html - register!
    /user - a quick summary. name & list of decks
    /user/settings.html - password and name
    /decks - list all of your decks with a create button
    / - ^
    /decks/<deckName> - do your SRS!
    /decks/<deckName>/edit -  edit the deck


it is you. your account. within is the decks. 


lets sketch the site.i


MONGODB!
    userId { "name",
             "password",
             "decks":
                    { chinese: {
                        front: {type: "" content ""}
                        back : {type: "" content ""}
                        }
                    }
            }

