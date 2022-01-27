import streamlit as st




def app(post_object, widget_id):
    ##### CREATE POST ENTRY
    with st.sidebar.expander(post_object.title):

        ##### DATE / TIME
        st.markdown(f"# {post_object.title}")
        st.markdown(f"### {post_object.date_to_post} @  {post_object.time_to_post} ({post_object.time_zone_to_post})")
        st.code(post_object.description)


        ########## MEDIAs
        #####

        ##### IMAGES
        attached_images = post_object.get_all_image_attachments()

        ##### Create a list of images
        if len(attached_images) > 0:

            st.caption("Images")

            for i in range(0, len(attached_images), 3):
                col1, col2, col3 = st.columns(3)
                try: 
                    with col1:
                        st.image(attached_images[i], width=85)
                    with col2:
                        st.image(attached_images[i+1], width=85)
                    with col3:
                        st.image(attached_images[i+2], width=85)
                except IndexError:
                    pass


        ##### VIDEO

        attached_videos = post_object.get_all_video_attachments()
        ##### Create a list of videos
        if len(attached_videos) > 0:
            
            st.caption("Videos")

            for i in range(0, len(attached_videos), 3):
                col1, col2, col3 = st.columns(3)
                try: 
                    with col1:
                        st.video(attached_videos[i], width=85)
                    with col2:
                        st.video(attached_videos[i+1], width=85)
                    with col3:
                        st.video(attached_videos[i+2], width=85)
                except IndexError:
                    pass


        ##### ALL

        ##### LIST ALL ATTACHMENTS AS FILES
        attached_files = post_object.load_attachments()
        st.caption("All Files")
        st.json(attached_files)


                
        ########## POST RESCHEDULE & CANCEL
        #####
        col1,col2,col3 = st.columns(3)

        ##### RESCHEDULE
        def reschedule_btn_react():
            print('button was clicked')

        ##### CANCEL
        def cancel_btn_react():
            was_canceled = post_object.remove_from_scheduled()
            if was_canceled:
                st.success("POST CANCELLED")
        

        ##### RESCHEDULE BUTTON
        with col1:
            reschedule_btn = st.button("Reschedule", widget_id, None, reschedule_btn_react)

        ##### CANCEL BUTTON
        with col3:
            cancel_btn = st.button("Cancel", widget_id, None, cancel_btn_react)
