import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\android\app\build.gradle")
t = io.open(p, encoding="utf-8").read()

if "packagingOptions" not in t:
    t = t.replace(
        """    buildTypes {
        release {""",
        """    packagingOptions {
        jniLibs {
            // onnxruntime-android-qnn 把各代 Hexagon 后端全打进来了，共 115MB。
            // libQnnHtpPrepare 是离线模型准备工具（42MB），运行时用不到；
            // V68/V69 是更老的 SoC，Dsp/Gpu 我们也不用。
            // 7s Gen 4 落在 V73/V75 之间，两个都留着更稳。
            excludes += [
                    '**/libQnnHtpPrepare.so',
                    '**/libQnnGpu.so',
                    '**/libQnnCpu.so',
                    '**/libQnnDsp.so',
                    '**/libQnnDspV66Skel.so',
                    '**/libQnnDspV66Stub.so',
                    '**/libQnnHtpV68Skel.so',
                    '**/libQnnHtpV68Stub.so',
                    '**/libQnnHtpV69Skel.so',
                    '**/libQnnHtpV69Stub.so',
            ]
        }
    }
    buildTypes {
        release {""",
        1,
    )
    # 只留 arm64：32 位 arm 上跑 82M 模型没有意义
    t = t.replace("abiFilters 'arm64-v8a', 'armeabi-v7a'", "abiFilters 'arm64-v8a'")
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("packaging ok")
else:
    print("already patched")
