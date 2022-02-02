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
        attached_images = post_object.get_all_image_attachments()

        print(attached_images)

        # the attached images are the actual file contents. (which are currently encrypted .get_buffers())

        # for each image, we need to decrypt it and then display it
        for image in attached_images:
            image_file = open(image, "rb")
            print('image: ', image_file)
            # print contents of file
            image_file_contents = image_file.read()
            print('image_file_contents: ', image_file_contents)
            #decrypt the image
            decrypted_image = crypt.decrypt(image_file_contents)
            print('decrypted_image: ', decrypted_image)

            # convert the decrypted image to a PIL image
            decrypted_image_pil = Image.open(BytesIO(decrypted_image.decode()))

            #

            #convert string to bytes
            # convert bytes to buffer image

            # print('decrypted image type: ', type(BytesIO(decrypted_image)))

            # # convert bytes to image
            # image = Image.open(decrypted_image)
            

            # image_buffer = BytesIO(image)

            # print(image_buffer)
            # print
            st.image(decrypted_image_pil, width=300)


        ##### Create a list of images
        if len(attached_images) > 0:
            
            #bYTES = BytesIO(attached_images[0])

            #print(bYTES)

            check_image = open(attached_images[0], "rb")

            print(check_image)

            st.caption("Images")

            exit

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
