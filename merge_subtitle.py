import srt
import sys
import datetime

def merge_srt(subtitle1, subtitle2):
    # 合并两个字幕条目
    return srt.Subtitle(
        index=subtitle1.index,
        start=min(subtitle1.start, subtitle2.start),
        end=max(subtitle1.end, subtitle2.end),
        content=f"<b>{subtitle1.content}</b>\n<i>{subtitle2.content}</i>",
        proprietary='',
    )

def load_srt(filename):
    with open(filename, 'r', encoding='utf-8') as file:
        return list(srt.parse(file.read()))

def save_srt(subtitles, filename):
    with open(filename, 'w', encoding='utf-8') as file:
        file.write(srt.compose(subtitles))

def main(srt_file1, srt_file2, output_file):
    # 加载SRT文件
    subtitles1 = load_srt(srt_file1)
    subtitles2 = load_srt(srt_file2)

    merged_subtitles = []
    i, j = 0, 0
    while i < len(subtitles1) and j < len(subtitles2):
        if subtitles1[i].start - subtitles2[j].end < datetime.timedelta(seconds=1) and \
           subtitles2[j].start - subtitles1[i].end < datetime.timedelta(seconds=1):
            merged_subtitle = merge_srt(subtitles1[i], subtitles2[j])
            
            if (merged_subtitle.end - merged_subtitle.start) > datetime.timedelta(seconds=7):
                split_time = (merged_subtitle.start + merged_subtitle.end) / 2
                merged_subtitles.append(srt.Subtitle(
                    index=merged_subtitle.index,
                    start=merged_subtitle.start,
                    end=split_time,
                    content=merged_subtitle.content,
                    proprietary=''
                ))
                merged_subtitles.append(srt.Subtitle(
                    index=merged_subtitle.index,
                    start=split_time,
                    end=merged_subtitle.end,
                    content=merged_subtitle.content,
                    proprietary=''
                ))
            else:
                merged_subtitles.append(merged_subtitle)
            i += 1
            j += 1
        elif subtitles1[i].start < subtitles2[j].start:
            merged_subtitles.append(subtitles1[i])
            i += 1
        else:
            merged_subtitles.append(subtitles2[j])
            j += 1

    while i < len(subtitles1):
        merged_subtitles.append(subtitles1[i])
        i += 1
    while j < len(subtitles2):
        merged_subtitles.append(subtitles2[j])
        j += 1

    save_srt(merged_subtitles, output_file)
    print(f"合并的字幕已保存到 {output_file}\nThe merged subtitle files have been saved to {output_file}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("Usage: python merge_subtitle.py <srt_file1> <srt_file2> <output_file>")
    else:
        srt_file1 = sys.argv[1]
        srt_file2 = sys.argv[2]
        output_file = sys.argv[3]
        main(srt_file1, srt_file2, output_file)
