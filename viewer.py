# Import required libraries
import streamlit as st
import chromadb
import pandas as pd
from chromadb.config import Settings


# Initialize the ChromaDB client
def get_chroma_client():
    client = chromadb.HttpClient(
        host="assistant_archival_db",
        port=8000,
        settings=Settings(allow_reset=True, anonymized_telemetry=False),
    )

    return client


def main():
    client = get_chroma_client()
    view_database(client)


def view_database(client):
    collections = client.list_collections()  # get the list of collections
    print(collections)
    if not collections:  # check if collections list is empty
        st.write("There are no collections.")
        return

    collection_names = [
        col.name for col in collections
    ]  # get the names of the collections

    # use the names for the selectbox
    selected_collection_name = st.selectbox("Select a collection", collection_names)

    # get the selected collection object when needed
    selected_collection = client.get_collection(selected_collection_name)

    # Create a sidebar menu
    menu_options = [
        "Visualize Collection",
        "Add Item",
        "Update Item",
        "Delete Item",
    ]
    selected_option = st.sidebar.selectbox("Choose an action", menu_options)

    if selected_option == "Visualize Collection":
        visualize(selected_collection)

    elif selected_option == "Add Item":
        new_item_embedding = st.text_input("Enter the embedding of the new item:")
        new_item_metadata = st.text_input("Enter the metadata of the new item:")
        new_item_id = st.text_input("Enter the ID of the new item:")

        # Add new item to the collection
        if st.button("Add Item"):
            selected_collection.add(
                embeddings=[float(new_item_embedding)],
                metadatas={"meta": new_item_metadata},
                ids=new_item_id,
            )
            st.write(f"Item {new_item_id} has been added.")

    elif selected_option == "Update Item":
        # Update an existing item in the collection
        item_id_to_update = st.text_input("Enter the ID of the item to update:")
        updated_item_embedding = st.text_input(
            "Enter the updated embedding of the item:"
        )
        updated_item_metadata = st.text_input("Enter the updated metadata of the item:")
        if st.button("Update Item"):
            selected_collection.update(
                ids=item_id_to_update,
                embeddings=[float(updated_item_embedding)],
                metadatas={"meta": updated_item_metadata},
            )
            st.write(f"Item {item_id_to_update} has been updated.")

    elif selected_option == "Delete Item":
        # Delete an item from the collection
        item_id_to_delete = st.text_input("Enter the ID of the item to delete:")
        if st.button("Delete Item"):
            selected_collection.delete(ids=item_id_to_delete)
            st.write(f"Item {item_id_to_delete} has been deleted.")


def visualize(collection):
    df = pd.DataFrame.from_dict(collection.get())
    st.markdown("### Collection: **%s**" % collection.name)
    st.dataframe(df, width=1400)


if __name__ == "__main__":
    # Set app layout to wide
    st.set_page_config(layout="wide")

    main()
