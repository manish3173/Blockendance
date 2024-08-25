def find_records(form, blockchain):
    a=len(blockchain)
    print(a)
    c=0
    for block in blockchain:
        
        print(block.data)
        print(block.hash)
        condition = (block.data[0] == form.get("name") and
                    block.data[1] == form.get("date") and
                    block.data[2] == form.get("course") and
                    block.data[3] == form.get("year") and
                    len(block.data[4]) == int(form.get("number")))
        if condition:
            return block.data[4]
    return -1
