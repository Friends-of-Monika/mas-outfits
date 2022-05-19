

# Submod made with love by u/KventisAnM
# https://github.com/ImKventis
# https://www.reddit.com/user/KventisAnM



init -990 python in mas_submod_utils:
    Submod(
        author="Kventis",
        name="Outfit Selector",
        description="A submod that allows you to save and load monika outfits!",
        version="1.0.1",
        dependencies={},
        settings_pane=None,
        version_updates={}
    )

# Loading outfit jsons
# I'm not sure if 190 is the correct init level, but it works
init 190 python in kventis_outfit_submod:
    import os
    import json

    outfit_dir = os.path.join(renpy.config.basedir, "outfits")    

    outfit_files = None

    try:
        outfit_files = os.listdir(outfit_dir)
    except: 
        os.mkdir(outfit_dir)

    outfit_files = os.listdir(outfit_dir)

    
    outfits = {}

    outfit_menu_entries = []

    if len(outfit_files) != 0:
        for tf in outfit_files:
            # print tf
            if tf.endswith(".json") == False:
                continue
            try:
                f = open(os.path.join(outfit_dir, tf), "r")
                data = json.load(f)
                f.close()
                outfits[tf[:-5]] = data
                outfit_menu_entries.append((tf[:-5], tf[:-5], False, False))
               # print outfit_menu_entries[0][1]
            except Exception as e:
               # print e
               continue
   # print outfits

# Should run once on install with high aff
init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_outfit_installed",
            conditional="True",
            action=EV_ACT_QUEUE,
            aff_range=(mas_aff.NORMAL, None)
        )
    )

init 5 python:
    addEvent(
        Event(
              persistent.event_database,
              eventlabel="monika_outfit_installed_talk",
              prompt="Can you tell me about custom outfits?",
              category=['clothes'],
              pool=True,
              unlocked=True,
              aff_range=(mas_aff.NORMAL, None)
        ),
        markSeen=False
)

label monika_outfit_installed:
    m 1eua  "Hey, [player]."
    m 1wub "I see you have added new .rpy files! "
    extend 2dua  "Let me just see whats in there.{w=0.3}.{w=0.3}.{w=0.3}"
    m 3wua "Oh an outfit selector!"
    m 1eua "Make sure to thanks u/KventisAnM for me."
    m 3eua "Oh he left a message for you.  "
    extend 3sua  "\"If you have any questions or submod suggestions, feel free to message me on reddit.\""
    m 1gua "Well isn't that neat!"
    m 1hua "Thanks for adding this for me, [player]."
    m 1hubsb "I love you!~"
    return "love"

label monika_outfit_installed_talk:
    m 1eua "You want to hear about custom outfits?"
    m 1hua "Okay!"
    m 3eub "Just ask me anytime and I'll save the outfit and accessories I'm currently wearing."
    m 3eub "This will create a file, {nw}"
    extend 1hub "that I can load for you!"
    m 1eua "Just let me know if you want me to wear a custom outfit."
    return 

init 5 python:
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_outfit_save",
            prompt="Can you save an outfit?",
            category=['appearance', 'clothes'],
            pool=True,
            unlocked=True,
            aff_range=(mas_aff.NORMAL, None)
        ),
        markSeen=False
    )

label monika_outfit_save:
    $ import json
    $ import os
    
    m 1hua "Sure!"

    label ostart:
        pass

    # Get nae for file
    $ done = False
    while not done:
        python:
            out_name = ""
            out_name = mas_input(
                    "Enter a name for this outfit:",
                    allow="abcdefghijklmnopqrstuvwxyz ABCDEFGHIJKLMNOPQRSTUVWXYZ-_0123456789",
                    length=20,
                    screen_kwargs={"use_return_button": True}
                    )

        #Check if we should return
        if out_name == "cancel_input":
            m 1euc "Oh okay."
            return "prompt"
        elif out_name == "":
            m 2lusdla "..."
            m 1eka "I'm sorry, but I can't save an outfit with no name, [player]."
        else:
            $ done = True

    python: 
        outfit_file = os.path.join(kventis_outfit_submod.outfit_dir, out_name + ".json")

        file_exists = os.access(
                os.path.normcase(outfit_file),
                os.F_OK
            )

    if file_exists:
        m 1eka "I already have an outfit saved called '[out_name]'"
        m "Should I overwrite it?{nw}"
        $ _history_list.pop()
        menu:
            m "Should I overwrite it?{fast}"

            "Yes.":
                pass

            "No.":
                # Jump to beginning
                jump ostart
    
    m 2dua "Hold on a moment.{w=0.3}.{w=0.3}"
    python:
        out_data = {
            "hair": monika_chr.hair.name,
            "clothes": monika_chr.clothes.name,
        }

        # Much cleaner
        acs = monika_chr.acs[3] + monika_chr.acs[4] + monika_chr.acs[5] + monika_chr.acs[6] + monika_chr.acs[7] + monika_chr.acs[8] + monika_chr.acs[9] + monika_chr.acs[10] + monika_chr.acs[11] + monika_chr.acs[12] + monika_chr.acs[13]
        # Needs names not classes
        acs = map(lambda arg: arg.name, acs)
        out_data["acs"] = acs
        
        saved = False
        try:
            with open(outfit_file, "w+") as out_file:
                json.dump(out_data, out_file)
                out_file.close()
    
            kventis_outfit_submod.outfits[out_name] = out_data
            kventis_outfit_submod.outfit_menu_entries.append((out_name, out_name, False, False))
            saved = True
        except Exception as e:
            saved = False

    if saved:
        m 3eub "Outfit saved!"
        return
    else:
        m 2eksdlc "I'm sorry [player], but I can't save the file."
        m 1eksdlc "Maybe try with a different name."
    return

init 5 python: 
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_outfit_load",
            prompt="Can you wear an outfit?",
            category=['appearance', 'clothes'],
            pool=True,
            aff_range=(mas_aff.NORMAL, None),
            unlocked=True
        ),
        markSeen=False
    )

# Needs testing
label monika_outfit_missing:
    m "[player].."
    m "I'm missing part of my outfit!"
    m "Did you remove it?"
    call mas_transition_from_emptydesk
    pause 1
    m 2dkd "I really liked that outfit too.."
    m 2ekd "Please re-add it!"
    return

# Needs testing
label monika_outfit_done_no_acs:

    $ import random

    pause 2

    m "Okay."

    call mas_transition_from_emptydesk

    pause 0.5

    m 4eublb "Tada!~"

    m 1euc "I am missing some accessories!"

    m 1ekc "Make sure to re-add them please."
    return


label monika_outfit_done:

    $ import random

    pause 2

    m "Okay."

    call mas_transition_from_emptydesk

    pause 1

    m 4eublb "Tada!~"

    # Cba to write quips tbh
    # $ quip = random.choice(kventis_outfit_submod.outfit_quips)

    # # Nomrmal "M "Dialoug"" wouldnt format quips for some reason
    # $ renpy.say(m, quip)
    return

label monika_outfit_load:

    m 1hua "Sure!"

    if len(kventis_outfit_submod.outfit_menu_entries) > 0:


        show monika at t21
        m 1eub "Which outfit do you want me to wear?" nointeract
        
        call screen mas_gen_scrollable_menu(kventis_outfit_submod.outfit_menu_entries, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, ("Nevermind", "Nevermind", False, False, 20))

        $ sel_outfit_name = _return

        show monika at t11

        if sel_outfit_name == "Nevermind":
            m 1euc "Oh okay."
            return "prompt"

        m 2dua "Hold on a moment.."

        call mas_transition_to_emptydesk

        pause 2

        python: 
            # Get all atrributes of outfit fills with None if missing
            # Dont have to check if new_clothes and new_hair in json dict as they always are.
            sel_outfit = kventis_outfit_submod.outfits[sel_outfit_name]
            new_clothes = mas_sprites.CLOTH_MAP.get(sel_outfit.get("clothes"), None)
            new_hair = mas_sprites.HAIR_MAP.get(sel_outfit.get("hair"), None)
            new_acs = monika_chr.acs[0] + monika_chr.acs[1] + monika_chr.acs[2]
            missing_acs = False

            for item in sel_outfit.get("acs", []):
                new_item = mas_sprites.ACS_MAP.get(item, None)
                if new_item != None:
                    new_acs.append(new_item)
                else:
                    missing_acs = True

        # Game assessts r missing
        if new_clothes == None or new_hair == None:
            call monika_outfit_missing
            return

        python: 
            monika_chr.remove_all_acs()
            monika_chr.change_clothes(new_clothes, True)
            monika_chr.change_hair(new_hair, True)
            # Applies all acs including the acs that were already on the table
            for ac in new_acs:
                monika_chr.wear_acs(ac)

        if missing_acs:
            call monika_outfit_done_no_acs
            return
        else:
            call monika_outfit_done
        return
    else:
        m 1euc "Oh wait."
        m 3lksdlb "Aha.. I don't have any outfits saved yet."
        m 1eub "Just let me know if you want an outfit saved."
        return

init 5 python: 
    addEvent(
        Event(
            persistent.event_database,
            eventlabel="monika_outfit_delete",
            prompt="Can you delete an outfit?",
            category=['appearance', 'clothes'],
            pool=True,
            aff_range=(mas_aff.NORMAL, None),
            unlocked=True
        ),
        markSeen=False
    )

label monika_outfit_delete:
    $ import os
    m 1hua "Sure!"

    if len(kventis_outfit_submod.outfit_menu_entries) > 0:


        show monika at t21
        m 1eub "Which outfit do you want me to delete?" nointeract
        
        call screen mas_gen_scrollable_menu(kventis_outfit_submod.outfit_menu_entries, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, ("Nevermind", "Nevermind", False, False, 20))

        $ sel_outfit_name = _return

        show monika at t11

        if sel_outfit_name == "Nevermind":
            m 1etc "Okay,{w=0.4} {nw}"
            extend 1hua "No outfits deleted!"
            return "prompt"
        
        m 1eksdlc "Are you sure you want to delete [sel_outfit_name], [player]? "
        extend "I cant undo this afterwards!{nw}"
        $ _history_list.pop()
        menu: 
            m "Are you sure you want to delete [sel_outfit_name], [player]? I cant undo this afterwards!{fast}"
            "I'm sure.":
                m "Okie dokie."
                python: 
                    removed = False
                    try:
                        os.remove(os.path.join(kventis_outfit_submod.outfit_dir, sel_outfit_name + ".json"))
                        kventis_outfit_submod.outfit_menu_entries.remove((sel_outfit_name, sel_outfit_name, False, False))
                        kventis_outfit_submod.outfits.pop(sel_outfit_name)
                        removed = True
                    except: 
                        removed = False
                m 2dua "Hold on a moment.{w=0.3}.{w=0.3}"
                if removed:
                   m 3eub "[sel_outfit_name] deleted!"
                else:
                    m 1euc "I couldn't find the file for [sel_outfit_name]!"
                    m 3lksdlb "You can maually delete it from the folder. "
                    m extend "It's called '[sel_outfit_name].json' in the folder 'outfits'!"
                return

            "Wait, I'm not sure.":
                m 1eusdlb "Aha, okay."
                return
    else:
        m 1euc "Oh wait."
        m 3lksdlb "Aha.. I don't have any outfits saved yet."
        m 1eub "Just let me know if you want an outfit saved."
        return

# G'day
# - British man
