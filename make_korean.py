
import os
import struct

# 1. 번역할 단어장 (왼쪽: 영어 원문 / 오른쪽: 한국어)
# 형님이 추가한 'BTCmobick'도 여기에 넣었습니다.
translations = {
    # [메인 메뉴]
    "Scan": "스캔",
    "Seeds": "시드(Seeds)",
    "Tools": "도구",
    "Settings": "설정",
    "Power": "전원",
    
    # [설정 메뉴]
    "Donate": "후원",
    "BTCmobick": "비트모빅 (BTCmobick)",  # 형님이 바꾼 제목
    "About": "정보",
    "I/O Test": "입출력 테스트",
    
    # [공통 동작]
    "Home": "홈",
    "Back": "뒤로",
    "Cancel": "취소",
    "Continue": "계속",
    "Done": "완료",
    "Yes": "예",
    "No": "아니요",
    
    # [입력/키보드]
    "Enter Passphrase": "패스프레이즈 입력",
    "Enter Seed Word": "시드 단어 입력",
    
    # [기타 메시지]
    "Loading...": "로딩 중...",
    "Camera": "카메라",
    "Mnemonic": "니모닉",
}

def create_mo_file(translations, output_path):
    # .mo 파일 헤더 매직 넘버
    MAGIC = 0x950412de
    VERSION = 0
    
    # 데이터 준비
    keys = sorted(translations.keys())
    original_strings = ''.join([k + '\x00' for k in keys]).encode('utf-8')
    translated_strings = ''.join([translations[k] + '\x00' for k in keys]).encode('utf-8')
    
    num_strings = len(keys)
    
    # 오프셋 계산
    key_offsets = []
    val_offsets = []
    
    current_key_offset = 28 + (num_strings * 16) # 헤더 + 테이블 크기
    current_val_offset = current_key_offset + len(original_strings)
    
    for k in keys:
        k_len = len(k.encode('utf-8'))
        v_len = len(translations[k].encode('utf-8'))
        
        key_offsets.append((k_len, current_key_offset))
        val_offsets.append((v_len, current_val_offset))
        
        current_key_offset += k_len + 1
        current_val_offset += v_len + 1

    # 파일 쓰기
    with open(output_path, 'wb') as f:
        # 헤더
        f.write(struct.pack('I', MAGIC))      # magic
        f.write(struct.pack('I', VERSION))    # version
        f.write(struct.pack('I', num_strings)) # number of strings
        f.write(struct.pack('I', 28))         # offset of table with original strings
        f.write(struct.pack('I', 28 + (num_strings * 8))) # offset of table with translation strings
        f.write(struct.pack('I', 0))          # size of hashing table
        f.write(struct.pack('I', 0))          # offset of hashing table
        
        # 원본 문자열 테이블 (길이, 오프셋)
        for length, offset in key_offsets:
            f.write(struct.pack('II', length, offset))
            
        # 번역 문자열 테이블 (길이, 오프셋)
        for length, offset in val_offsets:
            f.write(struct.pack('II', length, offset))
            
        # 실제 문자열 데이터
        f.write(original_strings)
        f.write(translated_strings)

    print(f"✅ 성공! 한글 파일 생성됨: {output_path}")

# 실행
if __name__ == "__main__":
    # 저장할 위치 (자동으로 폴더가 없으면 만듭니다)
    output_dir = "src/seedsigner/resources/seedsigner-translations/l10n/ko/LC_MESSAGES"
    os.makedirs(output_dir, exist_ok=True)
    
    output_file = os.path.join(output_dir, "messages.mo")
    create_mo_file(translations, output_file)