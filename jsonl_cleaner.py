import json

def clean_jsonl(input_file, output_file):
    """
    清洗 RAG 评测语料 (L1) 中的无效 Query
    规则：过滤掉长度小于 3 的单字或纯符号 Query，防止索引库被污染。
    """
    valid_count = 0
    
    with open(input_file, 'r', encoding='utf-8') as fin, \
         open(output_file, 'w', encoding='utf-8') as fout:
        
        for line in fin:
            try:
                data = json.loads(line.strip())
                query = data.get("query", "")
                
                # 核心降噪逻辑：剔除极短 Query (对应 SOP A - Step 1)
                if len(query.strip()) > 2:
                    fout.write(json.dumps(data, ensure_ascii=False) + '\n')
                    valid_count += 1
            except json.JSONDecodeError:
                continue # 物理跳过损坏的 JSON 行

    print(f"清洗完成！共保留 {valid_count} 条高质量真实语料。")

if __name__ == "__main__":
    print("初始化 AscendC L1 语料清洗管道...")
