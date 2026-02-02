import sys
sys.stdout = open('test_output.txt', 'w')

import chromadb
print('1. ChromaDB imported')

try:
    client = chromadb.PersistentClient(path='output/vector_db/chroma')
    print('2. Client created')
    
    collection = client.get_collection(name='rbac_chunks')
    print('3. Collection obtained')
    
    count = collection.count()
    print('4. Count:', count)
    
    sample = collection.get(limit=1)
    print('5. Sample retrieved')
    print('6. IDs:', sample['ids'])
    print('7. Metadatas:', sample['metadatas'])
    print('8. Documents:', [d[:50] for d in sample['documents']])
    
except Exception as e:
    print('ERROR:', str(e))

sys.stdout.close()
