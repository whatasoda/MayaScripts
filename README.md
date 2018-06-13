# MayaScripts

MayaでVR用の静止画像をレンダリングするためのレンズオブジェクトを生成するpythonです。

[coreEngProSAG2-VR](https://github.com/whatasoda/coreEngProSAG2-VR)で左目用と右目用の画像を用意する必要があったので書きました。

効果は[coreEngProSAG2-VR](https://github.com/whatasoda/coreEngProSAG2-VR)のVRモード（右下のハコスコアイコンをクリック）で五重塔の頂点あたりを見ていただければなんとなくわかると思います。

Mayaのplugin的なものを作れればよかったのですが、そこまでのことをする技術力が当時なかったので代替手段としてこの方法を取りました。実際のレンダリングでは屈折の計算などを挟むことになるのでレンズ無しのレンダリングよりもかなり時間がかかってしまいます。
