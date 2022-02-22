from multiprocessing.dummy import current_process
import streamlit as st
# imports BytesIO
from io import BytesIO
from resources.config import settings_core
from PIL import Image


settings = settings_core()

def app(post_object, widget_id):
    ##### CREATE POST ENTRY
    with st.sidebar.expander(post_object.title):

        ##### DATE / TIME
        # progress bar
        loading_progress = st.progress(0)
        st.markdown(f"# {post_object.title}")
        st.markdown(f"### {post_object.date_to_post} @  {post_object.time_to_post} ({post_object.time_zone_to_post})")
        st.code(post_object.description)
        
        ## Progress
        loading_progress.progress(5)
        current_progress = 5
        download_section_progress_worth = 35
        decryption_section_progress_worth = 60

        ########## MEDIAs
        #####
        with st.spinner("Loading Media..."):

            ## Get all attachments
            # Images
            attached_images = post_object.get_all_image_attachments()
            attached_images_length = len(attached_images)
            current_progress += download_section_progress_worth/3
            loading_progress.progress(int(current_progress))
            # Videos
            attached_videos = post_object.get_all_video_attachments()
            attached_videos_length = len(attached_videos)
            current_progress += download_section_progress_worth/3
            loading_progress.progress(int(current_progress))
            # Audio
            attached_audio = post_object.get_all_audio_attachments()
            attached_audio_length = len(attached_audio)
            current_progress += download_section_progress_worth/3
            loading_progress.progress(int(current_progress))


  

            total_length = 0

            ## Calculate progress percentage for each section
            if attached_images_length > 0:
                total_length += attached_images_length + 1
                
            if attached_videos_length > 0:
                total_length += attached_videos_length + 1
            
            if attached_audio_length > 0:
                total_length += attached_audio_length + 1

            if total_length > 0:
                per_section_progress_worth = decryption_section_progress_worth / total_length
            else:
                per_section_progress_worth = 100


        
        ##### LIST ALL ATTACHMENTS AS FILES
        attached_files = post_object.load_attachments()
        
        if attached_files:
            st.caption(f"All Files")
            attached_files_length = len(attached_files)
            st.markdown(f"Total of `{attached_files_length}`")


        
        ##### IMAGES
        with st.spinner("Processing Images..."):

            ## Get all image attachments
            
            decrypted_images = []

            ## Loop through Images
            for image in attached_images:



                ## Decrypt Image
                decrypted_image = BytesIO()

                ## Open file decrypt the contents 
                with settings.storage.open_file(image, "rb") as input_stream:
                    settings.crypt.decrypt_stream(input_stream, decrypted_image)

                ## Append decrypted contents to an array for reference
                decrypted_images.append(decrypted_image)

                ## Display Progress
                current_progress += per_section_progress_worth
                loading_progress.progress(int(current_progress))

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

                ##### DISPLAY PROGRESS
                current_progress += per_section_progress_worth
                loading_progress.progress(int(current_progress))



        ##### VIDEO
        with st.spinner("Loading Videos..."):

            ## Get all video attachments
            
            decrypted_videos = []
            

            ## Loop through Videos
            for video in attached_videos:

                ## Display Progress
                current_progress += per_section_progress_worth
                loading_progress.progress(int(current_progress))

                ## Decrypt Video
                decrypted_video = BytesIO()

                ## Open file decrypt the contents
                with settings.storage.open_file(video, "rb") as input_stream:
                    settings.crypt.decrypt_stream(input_stream, decrypted_video)

                ## Append decrypted contents to an array for reference
                decrypted_videos.append(decrypted_video)

            ## Create a list of videos from decrypted videos, closing each video as we go.
            if len(decrypted_videos) > 0:
                st.caption("Videos")
                for video in decrypted_videos:
                    st.video(video)
                    video.close()

                ##### DISPLAY PROGRESS
                current_progress += per_section_progress_worth
                loading_progress.progress(int(current_progress))
            
        
        #####
        with st.spinner("Loading Audio..."):

            ## Get all audio attachments
            decrypted_audios = []

            ## Loop through Audios
            for audio in attached_audio:

                ## Display Progress
                current_progress += per_section_progress_worth
                loading_progress.progress(int(current_progress))

                ## Decrypt Audio
                decrypted_audio = BytesIO()


                ## Open file decrypt the contents
                with settings.storage.open_file(audio, "rb") as input_stream:
                    settings.crypt.decrypt_stream(input_stream, decrypted_audio)
                
                
                ## Append decrypted contents to an array for reference
                decrypted_audios.append(decrypted_audio)

            ## Create a list of audios from decrypted audios, closing each audio as we go.
            if len(decrypted_audios) > 0:
                st.caption("Audio")
                for audio in decrypted_audios:
                    st.audio(audio)
                    audio.close()

                ##### DISPLAY PROGRESS
                current_progress += per_section_progress_worth
                loading_progress.progress(int(current_progress))

        ##### ALL
        st.json(attached_files)
        loading_progress.empty()
                
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
