

# Submod made with love by u/KventisAnM
# https://github.com/ImKventis
# https://www.reddit.com/user/KventisAnM



init -990 python in mas_submod_utils:
    Submod(
        author="Kventis",
        name="Outfit Selector",
        description="A submod that allows you to save and load monika outfits!",
        version="0.0.2",
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

    outfit_files = os.listdir(outfit_dir)

    outfits = {}

    outfit_menu_entries = []

    outfit_quips = ["I love this outfit!", "Good choice, [player].", "Thank you for this outfit, [player]."]

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

label monika_outfit_installed:
    m  "Hey, [player]!"
    m "I see you have added new .rpy files.."
    m "Let me just see whats in there..{w=0.3}..{w=0.3}..{w=0.3}"
    m "Oh an outfit selector!"
    m "Make sure to thanks u/KventisAnM for me.{nw}"
    m "If you have any questions or submod suggestions, feel free to message him on reddit."
    m "Thanks for adding this for me, [player]."
    m "I love you!~"
    return 'love'

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
    m "Awesome!"

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
            m "Oh okay"
            return
        elif out_name == "":
            m "..."
            m "I'm sorry, but I can't save an outfit with no name, [player]."
            # Change to say something ( ͡° ͜ʖ ͡°)
        else:
            $ done = True

    python: 
        outfit_file = os.path.join(kventis_outfit_submod.outfit_dir, out_name + ".json")

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
                # Jump to beginning
                jump ostart

    python:
        out_data = {
            "hair": monika_chr.hair.name,
            "clothes": monika_chr.clothes.name,
        }


        acs = []


        # Monika_chr.acs is a huge dict of lists
        # Unsure if I got this right

        if len(monika_chr.acs[3]) > 0:
            acs.append(monika_chr.acs[3][0].name)

        if len(monika_chr.acs[10]) > 0:
            acs.append(monika_chr.acs[10][0].name)
        out_data["acs"] = acs

        for item in monika_chr.acs[5]:
            acs.append(item.name)

        saved = False
        try:
            with open(outfit_file, "w+") as out_file:
                json.dump(out_data, out_file)
                out_file.close()
    
            kventis_outfit_submod.outfits[out_name] = out_data
            kventis_outfit_submod.outfit_menu_entries.append((out_name, out_name, False, False))
            saved = True
        except: 
            saved = False

    if saved:
        m "Outfit saved!"
        return
    else:
        m "I'm sorry [player], but I can't save the file."
        m "Maybe try with a different name."
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
    m "I really liked that outfit too.."
    m "Please re-add it!"
    return

# Needs testing
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


label monika_outfit_done:

    $ import random

    pause 2

    m "Okay."

    call mas_transition_from_emptydesk

    pause 0.5

    m "Tada!~"

    $ quip = random.choice(kventis_outfit_submod.outfit_quips)

    # Nomrmal "M "Dialoug"" wouldnt format quips for some reason
    $ renpy.say(m, quip)
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
            m "Oh okay."
            return

        m "Hold on a moment.."

        call mas_transition_to_emptydesk

        pause 2

        python: 
            # Get all atrributes of outfit fills with None if missing
            # Dont have to check if new_clothes and new_hair in json dict as they always are.
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

        # Game assessts r missing
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
        
        m "Are you sure you want to delete [sel_outfit_name], [player]? "
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
                m "Hold on a moment.{w=0.3}.{w=0.3}"
                if removed:
                    m "[sel_outfit_name] deleted!"
                else:
                    m "I couldn't find the file for [sel_outfit_name]!"
                    m "You can maually delete it from the folder. "
                    m extend "It's called outfits!"
                return

            "Wait, I'm not sure.":
                m "Aha, okay."
                return
    else:
        m "Oh wait."
        m "Aha.. I don't have any outfits saved yet."
        m "Just let me know if you want an outfit saved."
        return

# G'day
