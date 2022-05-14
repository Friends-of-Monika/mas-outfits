

# Second Submod made by u/KventisAnM
# https://github.com/ImKventis



init -990 python in mas_submod_utils:
    Submod(
        author="Kventis",
        name="Outfit Selector",
        description="A submod that allows you to save monika outfits!",
        version="0.0.1",
        dependencies={},
        settings_pane=None,
        version_updates={}
    )

init 190 python in kventis_outfit_submod:
    import os
    import json

    outfit_dir =  "outfits/" 

    outfit_files = os.listdir(outfit_dir)

    outfits = {}

    outfit_menu_entries = []

    outfit_quips = ["I love this outfit!", "Good choice, [player].", "Thank you for this outfit, [player]."]

    if len(outfit_files) != 0:
        for tf in outfit_files:
            print tf
            if tf.endswith(".json") == False:
                continue
            try:
                f = open(outfit_dir + tf, "r")
                data = json.load(f)
                f.close()
                outfits[tf[:-5]] = data
                outfit_menu_entries.append((tf[:-5], tf[:-5], False, False))
                print outfit_menu_entries[0][1]
            except:
                continue

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

label monika_outfit_installed:
    m "Did you know you can save my outfits?"
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
    
    m "You want me to save my outfit?"
    m "Just so you know I cant save acs right now.. "

    label ostart:
        pass

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
            m "Oh okay"
            return
        elif out_name == "":
            m "..."
            m "I'm sorry, but I can't save an outfit with no name, [player]."
        else:
            $ done = True

    python: 

        outfit_file = kventis_outfit_submod.outfit_dir + out_name + ".json"

        file_exists = os.access(
                os.path.normcase(outfit_file),
                os.F_OK
            )

    if file_exists:
        m "I already have an outfit saved called '[out_name]'"
        m "Should I overwrite it?{nw}"
        $ _history_list.pop()
        menu:
            m "Should I overwrite it?{fast}"

            "Yes.":
                pass

            "No.":
                jump ostart

    python:
        out_data = {
            "hair": monika_chr.hair.name,
            "clothes": monika_chr.clothes.name,
        }


        g_acs = []


        if len(monika_chr.acs[3]) > 0:
            g_acs.append(monika_chr.acs[3][0].name)

        if len(monika_chr.acs[10]) > 0:
            g_acs.append(monika_chr.acs[10][0].name)
        out_data["acs"] = g_acs

        for item in monika_chr.acs[5]:
            g_acs.append(item.name)


        with open(outfit_file, "w+") as out_file:
            json.dump(out_data, out_file)
            out_file.close()

        kventis_outfit_submod.outfits[out_name] = out_data
        kventis_outfit_submod.outfit_menu_entries.append((out_name, out_name, False, False))
    m "Outfit saved!"
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

label monika_outfit_missing:
    m "[player].."
    m "I'm missing part of my outfit!"
    m "Did you remove it?"
    call mas_transition_from_emptydesk
    m "I really liked that outfit too.."
    m "Please re-add it!"
    return

label monika_outfit_done:

    $ import random

    pause 2

    m "Okay."

    call mas_transition_from_emptydesk

    pause 0.5

    m "Tada!~"

    $ quip = random.choice(kventis_outfit_submod.outfit_quips)

    $ renpy.say(m, quip)
    return

label monika_outfit_done_no_acs:

    $ import random

    pause 2

    m "Okay."

    call mas_transition_from_emptydesk

    pause 0.5

    m "Tada!~"

    m "Oh, I am missing some accessories!"

    m "Make sure to re-add them for this outfit!"
    return

label monika_outfit_load:

    m "Sure!"

    if len(kventis_outfit_submod.outfit_menu_entries) > 0:


        show monika at t21
        m "What outfit do you want me to wear?" nointeract
        
        call screen mas_gen_scrollable_menu(kventis_outfit_submod.outfit_menu_entries, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, ("Nevermind", "Nevermind", False, False, 20))

        $ sel_outfit_name = _return

        show monika at t11

        if sel_outfit_name == "Nevermind":
            m "Okay, I'll keep my current outfit."
            return

        m "Hold on a moment.."

        call mas_transition_to_emptydesk

        pause 2

        python: 
            sel_outfit = kventis_outfit_submod.outfits[sel_outfit_name]
            new_clothes = mas_sprites.CLOTH_MAP.get(sel_outfit.get("clothes"), None)
            new_hair = mas_sprites.HAIR_MAP.get(sel_outfit.get("hair"), None)
            new_acs = []
            missing_acs = False

            for item in sel_outfit.get("acs", []):
                new_item = mas_sprites.ACS_MAP.get(item, None)
                if new_item != None:
                    new_acs.append(new_item)
                else:
                    missing_acs = True

        if new_clothes == None or new_hair == None:
            call monika_outfit_missing
            return

        python: 
            monika_chr.remove_all_acs()
            monika_chr.change_clothes(new_clothes, True)
            monika_chr.change_hair(new_hair, True)
            for ac in new_acs:
                monika_chr.wear_acs(ac)

        if missing_acs:
            call monika_outfit_done_no_acs
            return
        else:
            call monika_outfit_done
        return
    else:
        m "Oh wait."
        m "Aha.. I don't have any outfits saved yet."
        m "Just let me know if you want an outfit saved."
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
    m "Sure!"

    if len(kventis_outfit_submod.outfit_menu_entries) > 0:


        show monika at t21
        m "What outfit do you want me to delete?" nointeract
        
        call screen mas_gen_scrollable_menu(kventis_outfit_submod.outfit_menu_entries, mas_ui.SCROLLABLE_MENU_TXT_MEDIUM_AREA, mas_ui.SCROLLABLE_MENU_XALIGN, ("Nevermind", "Nevermind", False, False, 20))

        $ sel_outfit_name = _return

        show monika at t11

        if sel_outfit_name == "Nevermind":
            m "Okay, I wont delete any outfits."
            return

        m "Are you sure you want to delete this outfit, [player]?"
        m "I cant undo this afterwards!{nw}"
        $ _history_list.pop()
        menu: 
            m "I cant undo this afterwards!{fast}"
            "I'm sure.":
                m "Okay, I'll delete it."
                python: 
                    os.remove(kventis_outfit_submod.outfit_dir + sel_outfit_name + ".json")
                    kventis_outfit_submod.outfit_menu_entries.remove((sel_outfit_name, sel_outfit_name, False, False))
                    kventis_outfit_submod.outfits.pop(sel_outfit_name)
                m "Hold on a moment.{w=0.3}.{w=0.3}"
                m "Okay, I deleted it."
                return

            "Wait, I'm not sure.":
                m "Aha, okay."
                return
    else:
        m "Oh wait."
        m "Aha.. I don't have any outfits saved yet."
        m "Just let me know if you want an outfit saved."
        return


# Monika leaves the desk
# call mas_transition_to_emptydesk

# Monika sits down at the desk
# call mas_transition_from_emptydesk(exp)


# Notes 

#monika_chr = monika
# monika_chr.acs
# Maps 
    # mas_selspr.ACS_SEL_MAP
    # mas_selspr.HAIR_SEL_MAP
    # mas_selspr.CLOTH_SEL_MAP

# Use map to get clothes by name
# Holy fuck this too way too long to find
# $ print mas_selspr.CLOTH_SEL_MAP.get(monika_chr.clothes.name).name


    # python: 

    #     to_write = {}
    #     to_write["hair"] = monika_chr.hair.name
    #     to_write["clothes"] = monika_chr.clothes.name
    #     try: 
    #         outfit_output = open(config.basedir + "/outfits/{}.json".format(out_name), "w+")
    #         json.dump(to_write, outfit_output)
    #         outfit_output.close()
    #     except:
    #         renpy.say(m, "I'm sorry [player]..")
    #         renpy.say(m , "I couldn't save the outfit")



        #     def change_clothes(
        #         self,
        #         new_cloth,
        #         by_user=None,
        #         startup=False,
        #         outfit_mode=False
        # ):
        #     """
        #     Changes clothes to the given cloth. also sets the persistent
        #     force clothes var to by_user, if its not None
        #     IN:
        #         new_cloth - new clothes to wear
        #         by_user - True if this action was mandated by the user, False
        #             if not. If None, we do NOT set the forced clothes var
        #             (Default: None)
        #         startup - True if we are loading on startup, False if not
        #             When True, we dont respect locking
        #             (Default: False)
        #         outfit_mode - True means we should change hair/acs if it
        #             completes the outfit. False means we should not.
        #             NOTE: this does NOT affect hair/acs that must change for
        #                 consistency purposes.
        #             (Default: False)
        #     """