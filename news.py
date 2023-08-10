import streamlit as st
import requests
from bs4 import BeautifulSoup
from langchain import PromptTemplate, LLMChain
from langchain.chat_models import ChatOpenAI
import datetime

content1 = "Apple is reportedly prepping for an iPhone 15 Pro event on September 13. According to information seen by 9to5Mac, mobile carriers have been asking employees not to take days off on September 13 due to a major smartphone announcement. The event is expected to announce the new iPhones, which will feature a new design with slightly curved edges and thinner bezels around the display, Dynamic Island and USB-C instead of Lightning, and a new periscope lens for better optical zoom on the Pro models. Pre-orders are expected to begin on September 15, with the official launch a week later on September 22. Prices of the new iPhones may rise by up to $200 compared to the current generation."  # noqa: E501

content2 = """Harmonyos 放肆玩亠起玩 有个性 全新的设计让你的照片、心情 甚至是自然天气都能成为你个性的完美表达 艺术主角’ 智能识别画面主体 多样艺术背景随心搭 海报标题’ 字体设计更多元 (i26 全新Emoji表情’ 情绪表达更多样 时尚画册’ 杂志化布局 0g:0g 趣味心情主题’ 把你的心情设省成主题 全景天气壁纸” 将自然天气装进手机，实时感知天气变化 Harmonyos 4趣味主题‘ 可爱胜胀风，更立体更好玩 (08:0g 更高效 信息处理和内容分享变得更加高效便捷 实况窗 任务进度随时掌握，可大可小可交互 更多设备更高效 弦月窗° 实时任务状态，拾腕便知 生道费中 𣊭 全新通知中心 “置顶"关键信息 轻重缓急一目了然 超级中转站° 双指长按 提取文本图片 更多应用随手拖入 多屏同享 音画同步 座舱也能一起看大片 演示批注° 可圈点可标注，多种文档不限应用 手写批注实时展示，会议交流高效轻松 游戏流转’ 痤舱畅玩手澼 航拍流转 手机航拍流转座舱 “大智慧 全新小艺，更聪明、更能干、更贴心 更聪明 智慧交互 更贴心 个性化服务 从准确指令 到自然对话 随口记事 适时提醒 全新小艺” 大有不同 好的．邦徐记佳了 场景化服务组合 每杂场景 轻松绾排 更能干 高效生产力 资讯内容 快速摘要 看图说话 服务直达 文家创作 内容辅助 照片趣玩 玩出创意 畅快玩 全新华为方舟引擎带来图形、多媒体、内存、调度、存储、低功耗 六大引擎技术，多设备也流畅 华为方舟引擎1。 图形 寧 多媒恷引擎 肉葆 𦘦 调度引禁 低功栝引禁 20 % 个 更流畅 30分钟个 更省电 超安心 风险更可视，用机更安心 全新应用管控中心。 更可视 更安心 新无风险 风險成用安装 拦截提醒 风险应用安装 自动管控。 风险应用安装 最小授予 凤險成用运行 主动抬截 应用跟踪管理。 是否允许应用跟踪你在其他应用和网站上的活动 由你说了算"""  # noqa: E501""

content3 = "Apple reported its third quarter results for fiscal 2023, ending July 1, 2023. The Company posted quarterly revenue of $81.8 billion, down 1 percent year over year, and quarterly earnings per diluted share of $1.26, up 5 percent year over year. Services revenue reached an all-time high, and the installed base of active devices set an all-time record. The board of directors declared a cash dividend of $0.24 per share of the Company’s common stock, payable on August 17, 2023. Apple also provided live streaming of its Q3 2023 financial results conference call. The Company is continuing to advance its values, while championing innovation that enriches the lives of customers and leaves the world better than it found it."  # noqa: E501

content4 = "AMD has announced the release of two new graphics cards, the Radeon Pro W7600 and W7500, as part of their mid-range professional video card lineup. These cards are based on AMD's RDNA 3 architecture and offer advanced features such as AV1 encoding support, improved compute and ray tracing throughput, and DisplayPort 2.1 outputs. The Radeon Pro W7600 is a full-height card with 32 compute units and a boost clock of 2.43GHz, while the W7500 is a sub-75W card that can be powered entirely by a PCIe slot. Both cards are expected to hit the market later this quarter."  # noqa: E501

content5 = "Nikon has issued an important notice to its users regarding a potential issue with the Z 8 digital mirrorless camera. Some users have reported that the camera strap lug may become loose or detach from the camera body under certain conditions. Nikon has identified the affected serial numbers and will provide free repairs and cover shipping costs, regardless of whether the camera is still under warranty. Users are advised to contact Nikon's customer support hotline or service centers for assistance. This issue also includes cameras that were previously identified for a different problem related to lens rotation."  # noqa: E501

content6 = " 一加手机岛 23-8-4 08:31 发布于广东 来自一加Ace2Pro 性能巅峰 淘汰 8GB， 12GB 起步， 16GB 普及， 24GB 引领，还有呢？ #一加Ace2Pro#，2023年8月，敬请期待。 关注＋转评，抽送一个一加真无线耳机。 8GB 淘汰 12GB 起步 116GB 普及 24GB 引领"  # noqa: E501


def loadWeb(url):
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
# Format the website content as text
    formatted_text = soup.get_text()
    content = ''.join(formatted_text.split(" "))
    content = ''.join(formatted_text.split("\n"))
    print(content)
    print("===")
    return content


def generate_news(url, content):
    prompt_template = """
    You are a good news writer. You can understand both English and Chinese very well. You are writing news in Chinese based on the content. Then content might be Chinese or English. You use markdown and add a link to the news. Excluding the url, ensure your answer is in 80-100 characters and contain details. Place one space between number and Chinese character. Ensure the accuracy and no misleading information. If the summary is not a news summary, return only NA.

URL: "https://9to5mac.com/2023/08/03/sources-iphone-15-event-september/",
summary: {content1},
answer:
[苹果](https://9to5mac.com/2023/08/03/sources-iphone-15-event-september/) 可能于 9 月 13 日召开秋季发布会，移动运营商强调员工不得在当天休假

URL:https://9to5mac.com/2023/08/03/sources-iphone-15-event-september/
summary: {content2}
answer:
[华为](https://weibo.com/3514064555/Nd1wycZaP) 发布鸿蒙 HarmonyOS 4 系统，新增实时活动，更新小艺 AI 并带来方舟引擎

URL:https://www.apple.com/newsroom/2023/08/apple-reports-third-quarter-results/
summary: {content3}
answer:
[苹果](https://www.apple.com/newsroom/2023/08/apple-reports-third-quarter-results/) 发布 2023 Q3 财报，营收 818 亿美元，同比下降 1%

URL:https://www.anandtech.com/show/19993/amd-announces-radeon-pro-w7600-w7500
summary: {content4}
answer:
[AMD](https://www.anandtech.com/show/19993/amd-announces-radeon-pro-w7600-w7500) 发布 Radeon PRO W7500 与 W7600 工作站显卡，售价为 $429 和 $599

URL:https://www.nikon.com.cn/sc_CN/service-and-support/service-advisory.tag/service_advisory_notices/service_advisory_for_z_8_1.dcr
summary: {content5}
answer:
[尼康](https://www.nikon.com.cn/sc_CN/service-and-support/service-advisory.tag/service_advisory_notices/service_advisory_for_z_8_1.dcr) 发布《致尊敬的尼康Z 8用户通知》，承认 Z 8 微单相机存在挂带孔松动问题，已启动召回程序


URL: https://weibo.com/3871046669/NcYF9pGgL
summary: {content6}
answer:
[一加](https://weibo.com/3871046669/NcYF9pGgL) 宣布为一加 Ace 2 Pro 手机推出 24GB 超大内存版本

URL: https://twitter.com/OpenAI/status/1687159114047291392
summary: Apologies, but I am unable to access the provided URL or any specific news content. However, I can still help you with any other questions or topics you may have.
answer:
NA

URL: {url7}
summary: {content7}
answer:

    """  # noqa: E501
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
    llm_chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate.from_template(prompt_template)
    )
    return llm_chain({"content1": content1,
                      "content2": content2, "content3": content3, "content4": content4,
                      "content5": content5, "content6": content6, "content7": content,
                      "url7": url})


def summary(url):
    content = "url\n"+loadWeb(url)
    prompt_template = "You are a good news writer. Summarize the following news in 100 words. Ensure you get the details and accuacy. Avoid misleadings. If the news is Chinese, the summary should be Chinese News: {news}"  # noqa: E501
    llm = ChatOpenAI(temperature=0, model_name="gpt-3.5-turbo-16k")
    llm_chain = LLMChain(
        llm=llm,
        prompt=PromptTemplate.from_template(prompt_template)
    )
    return llm_chain(content)


def generate_news_by_url(url, index=1):
    with st.spinner('生成新闻 '+str(index)+' 摘要中'):
        content = summary(url)
        st.subheader("新闻摘要 "+str(index))
        st.text(content["text"])
    with st.spinner('生成新闻 '+str(index)):
        news = generate_news(url, content)
        st.subheader("新闻 "+str(index))
        if news["text"] == "NA":
            st.write("无法抓取 URL 内容")
            st.write(url)
        else:
            st.write(news["text"])
    return news["text"]


def main():
    st.title("早晚报生成器（Alpha）")
    selector = st.selectbox("选择你的输入", ["多个URL", "URL", "报道"])
    if selector == "多个URL":
        text_input = st.text_area(
            label="输入多个 URL(Youtube, Weibo, Twitter,图片 等内容无法抓取)", value="https://twitter.com/OpenAI/status/1687159114047291392\nhttps://www.macrumors.com/2023/08/04/iphone-16-pro-stacked-camera-sensor/")
    else:
        text_input = st.text_input(f"输入你的 {selector}")

    if st.button("生成"):
        if selector == "URL":
            generate_news_by_url(text_input)
        elif selector == "多个URL":
            urls = text_input.split('\n')
            news_content = []
            my_bar = st.progress(0, text="生成早报中")
            for i in range(len(urls)):
                news = generate_news_by_url(urls[i], i+1)
                if news != "NA":
                    news_content.append(news)
                my_bar.progress(int((i+1)*100/len(urls)),
                                text="生成新闻 "+str(i+1))
            st.subheader("草稿")
            modified_news_content = []
            for i, element in enumerate(news_content):
                if i+1 == 1:
                    modified_element = "1️⃣ "+element
                elif i+1 == 2:
                    modified_element = "2️⃣ "+element
                elif i+1 == 3:
                    modified_element = "3️⃣ "+element
                elif i+1 == 4:
                    modified_element = "4️⃣ "+element
                elif i+1 == 5:
                    modified_element = "5️⃣ "+element
                elif i+1 == 6:
                    modified_element = "6️⃣ "+element
                elif i+1 == 7:
                    modified_element = "7️⃣ "+element
                elif i+1 == 8:
                    modified_element = "8️⃣ "+element
                elif i+1 == 9:
                    modified_element = "9️⃣ "+element
                modified_news_content.append(modified_element)

            news_content = "# News\n\n☀️ 自留地早报【" + \
                str(datetime.date.today().month) + "." + \
                str(datetime.date.today().day) + "】\n\n"
            news_content += "\n\n".join(modified_news_content)
            news_content += "\n\n频道：@ NewlearnerChannel"
            st.markdown(news_content)


if __name__ == "__main__":
    main()
