import streamlit as st
# imports BytesIO
from io import BytesIO
from resources.crypt import Key, Crypt
from resources.config import settings_core
from PIL import Image


settings = settings_core()

key = Key(settings.key_location)
crypt = Crypt(key, settings.block_size)

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
        with st.spinner("Loading Images..."):
            attached_images = post_object.get_all_image_attachments()
            decrypted_images = []

            ## For each image, decrypt & append to file for display
            for image in attached_images:
                decrypted_image = BytesIO()
                with open(image, "rb") as input_stream:
                    crypt.decrypt_stream(input_stream, decrypted_image)

                decrypted_images.append(decrypted_image)

            ##### Create a list of images from decrypted images, closing each image as we go.
            if len(decrypted_images) > 0:
                st.caption("Images")
                for i in range(0, len(decrypted_images), 3):
                    col1, col2, col3 = st.columns(3)
                    try: 
                        with col1:
                            if decrypted_images[i]:
                                decrypted_image_pil = Image.open(decrypted_images[i])
                                st.image(decrypted_image_pil, use_column_width='auto')
                                decrypted_images[i].close()
                        with col2:
                            if decrypted_images[i+1]:
                                decrypted_image_pil = Image.open(decrypted_images[i+1])
                                st.image(decrypted_image_pil, use_column_width='auto')
                                decrypted_images[i+1].close()
                        with col3:
                            if decrypted_images[i+2]:
                                decrypted_image_pil = Image.open(decrypted_images[i+2])
                                st.image(decrypted_image_pil, use_column_width='auto')
                                decrypted_images[i+2].close()
                    except IndexError:
                        pass


        ##### VIDEO
        with st.spinner("Loading Videos..."):
            attached_videos = post_object.get_all_video_attachments()
            decrypted_videos = []

            ## For each video, decrypt & append to file for display
            for video in attached_videos:
                decrypted_video = BytesIO()
                with open(video, "rb") as input_stream:
                    crypt.decrypt_stream(input_stream, decrypted_video)
                decrypted_videos.append(decrypted_video)

            ## Create a list of videos from decrypted videos, closing each video as we go.
            if len(decrypted_videos) > 0:
                st.caption("Videos")
                for video in decrypted_videos:
                    st.video(video)
                    video.close()
            
        
        #####
        with st.spinner("Loading Audio..."):
            attached_audios = post_object.get_all_audio_attachments()

            decrypted_audios = []

            ## For each audio, decrypt & append to file for display
            for audio in attached_audios:
                decrypted_audio = BytesIO()
                with open(audio, "rb") as input_stream:
                    crypt.decrypt_stream(input_stream, decrypted_audio)
                decrypted_audios.append(decrypted_audio)

            ## Create a list of audios from decrypted audios, closing each audio as we go.
            if len(decrypted_audios) > 0:
                st.caption("Audio")
                for audio in decrypted_audios:
                    st.audio(audio)
                    audio.close()

        ##### ALL

        ##### LIST ALL ATTACHMENTS AS FILES
        attached_files = post_object.load_attachments()
        
        if attached_files:
            st.caption(f"All Files")
            attached_files_length = len(attached_files)
            st.markdown(f"Total of `{attached_files_length}`")
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
