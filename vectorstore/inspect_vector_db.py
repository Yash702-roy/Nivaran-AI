import faiss
import pickle

# Load the FAISS index
index = faiss.read_index("vectorstore/nivaran.index")

print("Total vectors:", index.ntotal)
print("Dimensions:", index.d)

# Load the stored chunks
with open("vectorstore/chunks.pkl", "rb") as f:
    chunks = pickle.load(f)

print("Total chunks:", len(chunks))

# Display the first chunk
print("\nFirst chunk:")
print(chunks[0])

# Display the first vector
print("\nFirst vector:")
print(index.reconstruct(0))