import io
import pathlib

p = pathlib.Path(r"E:\flutter\open-deepseek\android\app\build.gradle")
t = io.open(p, encoding="utf-8").read()

if "onnxruntime" not in t:
    # 只打 arm 架构：手机端不需要 x86，能把 40MB 的运行时压掉一半
    t = t.replace(
        """        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner\"""",
        """        testInstrumentationRunner "androidx.test.runner.AndroidJUnitRunner"
        ndk {
            // 手机端只需要 arm；x86 只用于模拟器，本机禁开模拟器
            abiFilters 'arm64-v8a', 'armeabi-v7a'
        }""",
        1,
    )
    t = t.replace(
        """    implementation project(':capacitor-cordova-android-plugins')
}""",
        """    implementation project(':capacitor-cordova-android-plugins')
    // ONNX Runtime + Qualcomm QNN EP：Hexagon NPU 的唯一入口（HTP 后端）
    implementation "com.microsoft.onnxruntime:onnxruntime-android-qnn:1.20.0"
}""",
        1,
    )
    io.open(p, "w", encoding="utf-8", newline="\n").write(t)
    print("gradle deps ok")
else:
    print("already has onnxruntime")
