# 2D4Node_FEM
  Basic_2D3Node_FEMのv1.2.0より作成
  
  ![image](https://user-images.githubusercontent.com/88224293/167407874-bceb61c9-fef8-414f-9152-113319992733.png)

  
  
  # 変更点
  各エレメントに素材が追加
  4節点に変更




# Version1.0.0

# バグあり、使用禁止
#7 

# Version1.0.0概要



このプログラムは、
[Basic_2D3Node_FEM Version1.2.0](https://github.com/yuki-2000/Basic_2D3Node_FEM/releases/tag/v1.2.0)
をもとに、
[D-4NODE-ISOPARAMETRIC2.F90](https://github.com/yuki-2000/2D4Node_FEM/blob/main/2D-4NODE-ISOPARAMETRIC2.F90)
に従ってpythonに書き換えたプログラムです。


このプログラムは、
2次元4節点のアイソパラメトリック要素を使った有限要素法プログラムです。
また、各要素の素材を設定できるほか、等方材料だけでなく直交異方性材料にも対応しています。





## What's Changed
* Conform to 2 d4node by @yuki-2000 in https://github.com/yuki-2000/2D4Node_FEM/pull/6

## New Contributors
* @yuki-2000 made their first contribution in https://github.com/yuki-2000/2D4Node_FEM/pull/6

**Full Changelog**: https://github.com/yuki-2000/2D4Node_FEM/commits/v1.0.0


# 参考サイト
https://tex-image-link-generator.herokuapp.com/

https://qiita.com/damyarou/items/320bad2052bb5fccd75f#%E3%81%B2%E3%81%9A%E3%81%BF-%E5%A4%89%E4%BD%8D%E9%96%A2%E4%BF%82%E8%A1%8C%E5%88%97

http://www.ms1.mctv.ne.jp/sifoen.project/FEM/FEM-PDF/shape%20function%20&%20Jacobi%20matrix.pdf

http://www.multi.k.u-tokyo.ac.jp/lectures/H18_HPC/materials/FEM_2D.PDF

https://monoist.itmedia.co.jp/mn/articles/0909/02/news100_2.html




# Fortranからの変数名の変更


|  意味 |Fortran | このプログラム |
|---|-----|---|
|    素材数    |  MATERIAL | num_material   |
|    素材識別番号    |  mat_num | material   |
|  厚さ  |  h   |  thickness |
| 要素構成節点座標   | e_point  | e_node  |
| ヤコビ行列式 | det  |  det_Jacobi |
| 積分点 | gauss  | gauss_nodes|

# 2D3Node→2D4Nodeの変更点

### 全体
3節点から4節点に代わったため、3から4や6から8に行列のサイズが変わったりしている。


入力

### input_AnalysisConditions
3nodeからの変更
読み込む順番の変更
おそらく3Dになるときに厚さがなくなるため一番後ろに変更

### input_point
input_pointが、dを使った浮動小数かつスペース区切りになったので対応
入力input_elemeもスペース区切りになったので対応


### input_material
 input_materialが追加されたので読み取りを追加


### makeDmat
入力の形が最悪で、素材によって要素数が違うため、1行ずつ読まなければ


### makeKmat
material[i]は、i要素の素材番号1始まりだが、Dmatの格納場所は0なので注意

### 残り

makeFmat、makeUmat、makeSUBmatrix、makeInverse、solveUmat、solveFmat、に変更はなし。



### 可視化
可視化について、4角形はなかったのでこちらを参照
https://stackoverflow.com/questions/52202014/how-can-i-plot-2d-fem-results-using-matplotlib



# 解説

## input

今回のプログラムでは、'input_point.txt'と'input_eleme.txt'がカンマ区切りからスペース区切りに変更された。どっちが業界標準なのかわからない。前者に関しては、浮動小数dも使用されるようになった。

そして新しく追加された'input_material.txt'だが、これは要素番号、素材番号を表したファイルである。

## Dmat

今回の問題児。

### input_matinfo.txt

'input_matinfo.txt'があるのだが、これは1行目から順に、

```plane stress status
plane stress status: 1, plane strain status: 2　（1とする）

MATERIAL ID 
mat_type　Isotropic Material: 1, Transversely Isotropic Material: 2   (1とする)
Young1
Poisson1

MATERIAL ID 
mat_type　Isotropic Material: 1, Transversely Isotropic Material: 2 (2とする)
Young1    LL
Young2    TT
Poisson1  LT
Poisson2  TL
GL            LT

...
(空行は見やすいように今入れただけで、実際はない。)
```


```plane strain status
plane stress status: 1, plane strain status: 2　（2とする）

MATERIAL ID 
mat_type　Isotropic Material: 1, Transversely Isotropic Material: 2   (1とする)
Young1
Poisson1

MATERIAL ID 
mat_type　Isotropic Material: 1, Transversely Isotropic Material: 2 (2とする)
Young2   #TT
Poisson1 #LT
Poisson2 #TL
Poisson3 #TT
GL           #LT
...



(空行は見やすいように今入れただけで、実際はない。)
```

というように、情報が順番に書かれていく。


なお、
Lを繊維軸方向
Tを繊維軸直交方向
sotropic Material 等方材料
Transeversely Isotropic Material　直交異方性材料、横等方性材料


>L，Tがx，yのような座標軸を表していて，材料力学のひずみや応力の下付き添え字のルール同様，複数回重ねることで垂直，せん断方向を定義します．
L，Tに関しては，Lは強い（ヤング率が高い，強度が高い）方向，Tは弱い方向を指しています．
直交異方性材料では，方向によって材料定数が変わってくるのでこの様に表現しています．
我々の研究室では直交異方性材料は主に繊維や繊維束に対して仮定するので，Lを繊維軸方向，Tを繊維軸直交方向と考えることが多いです．


これが厄介で、素材によって書かれている行数が違うため、fortranのように1行ずつ読み込んでいかなければいけない。

### Dmat

今回は、おそらく炭素繊維を意識して、直交異方性材料を使用できるようにしている。


http://solid4.mech.okayama-u.ac.jp/%E5%BC%BE%E6%80%A7%E4%BD%93%E3%81%AE%E6%A7%8B%E6%88%90%E5%BC%8F.pdf


等方材料については以下であった。


#### 平面応力状態での応力ーひずみ関係式

![\begin{equation}
\begin{Bmatrix} \sigma_x \\ \sigma_y \\ \tau_{xy} \end{Bmatrix}
=\frac{E}{1-\nu^2}\begin{bmatrix} 1 & \nu & 0 \\ \nu & 1 & 0 \\ 0 & 0 & \cfrac{1-\nu}{2} \end{bmatrix}
\begin{Bmatrix} \epsilon_x \\ \epsilon_y \\ \gamma_{xy} \end{Bmatrix}
\end{equation}](https://render.githubusercontent.com/render/math?math=%5Ccolor%7Bblack%7D%5Cdisplaystyle+%5Cbegin%7Bequation%7D%0A%5Cbegin%7BBmatrix%7D+%5Csigma_x+%5C%5C+%5Csigma_y+%5C%5C+%5Ctau_%7Bxy%7D+%5Cend%7BBmatrix%7D%0A%3D%5Cfrac%7BE%7D%7B1-%5Cnu%5E2%7D%5Cbegin%7Bbmatrix%7D+1+%26+%5Cnu+%26+0+%5C%5C+%5Cnu+%26+1+%26+0+%5C%5C+0+%26+0+%26+%5Ccfrac%7B1-%5Cnu%7D%7B2%7D+%5Cend%7Bbmatrix%7D%0A%5Cbegin%7BBmatrix%7D+%5Cepsilon_x+%5C%5C+%5Cepsilon_y+%5C%5C+%5Cgamma_%7Bxy%7D+%5Cend%7BBmatrix%7D%0A%5Cend%7Bequation%7D)

#### 平面ひずみ状態での応力ーひずみ関係式

![\begin{equation}
\begin{Bmatrix} \sigma_x \\ \sigma_y \\ \tau_{xy} \end{Bmatrix}
=\frac{E}{(1+\nu)(1-2\nu)}\begin{bmatrix} 1-\nu & \nu & 0 \\ \nu & 1-\nu & 0 \\ 0 & 0 & \cfrac{1-2\nu}{2} \end{bmatrix}
\begin{Bmatrix} \epsilon_x \\ \epsilon_y \\ \gamma_{xy} \end{Bmatrix}
\end{equation}
](https://render.githubusercontent.com/render/math?math=%5Ccolor%7Bblack%7D%5Cdisplaystyle+%5Cbegin%7Bequation%7D%0A%5Cbegin%7BBmatrix%7D+%5Csigma_x+%5C%5C+%5Csigma_y+%5C%5C+%5Ctau_%7Bxy%7D+%5Cend%7BBmatrix%7D%0A%3D%5Cfrac%7BE%7D%7B%281%2B%5Cnu%29%281-2%5Cnu%29%7D%5Cbegin%7Bbmatrix%7D+1-%5Cnu+%26+%5Cnu+%26+0+%5C%5C+%5Cnu+%26+1-%5Cnu+%26+0+%5C%5C+0+%26+0+%26+%5Ccfrac%7B1-2%5Cnu%7D%7B2%7D+%5Cend%7Bbmatrix%7D%0A%5Cbegin%7BBmatrix%7D+%5Cepsilon_x+%5C%5C+%5Cepsilon_y+%5C%5C+%5Cgamma_%7Bxy%7D+%5Cend%7BBmatrix%7D%0A%5Cend%7Bequation%7D%0A)



しかし、直交異方性材料では以下のようになる。


### 平面応力状態

![\begin{equation}
\begin{Bmatrix} \sigma_x \\ \sigma_y \\ \tau_{xy} \end{Bmatrix}
=\begin{bmatrix} \frac{E_1}{1-\nu_12 \nu_21} & \frac{\nu_12 E_2}{1-\nu_12 \nu_21} & 0 \\ 
\frac{\nu_12 E_2}{1-\nu_12 \nu_21} & \frac{ E_2}{1-\nu_12 \nu_21} & 0 \\
 0 & 0 & G_12 \end{bmatrix}
\begin{Bmatrix} \epsilon_x \\ \epsilon_y \\ \gamma_{xy} \end{Bmatrix}
\end{equation}](https://render.githubusercontent.com/render/math?math=%5Ccolor%7Bblack%7D%5Cdisplaystyle+%5Cbegin%7Bequation%7D%0A%5Cbegin%7BBmatrix%7D+%5Csigma_x+%5C%5C+%5Csigma_y+%5C%5C+%5Ctau_%7Bxy%7D+%5Cend%7BBmatrix%7D%0A%3D%5Cbegin%7Bbmatrix%7D+%5Cfrac%7BE_1%7D%7B1-%5Cnu_12+%5Cnu_21%7D+%26+%5Cfrac%7B%5Cnu_12+E_2%7D%7B1-%5Cnu_12+%5Cnu_21%7D+%26+0+%5C%5C+%0A%5Cfrac%7B%5Cnu_12+E_2%7D%7B1-%5Cnu_12+%5Cnu_21%7D+%26+%5Cfrac%7B+E_2%7D%7B1-%5Cnu_12+%5Cnu_21%7D+%26+0+%5C%5C%0A+0+%26+0+%26+G_12+%5Cend%7Bbmatrix%7D%0A%5Cbegin%7BBmatrix%7D+%5Cepsilon_x+%5C%5C+%5Cepsilon_y+%5C%5C+%5Cgamma_%7Bxy%7D+%5Cend%7BBmatrix%7D%0A%5Cend%7Bequation%7D)


平面ひずみ状態については、調査中






## makeBmat 

今回の最難関
アイソパラメトリック要素とガウス・ルジャンドル数値積分について


![image](https://user-images.githubusercontent.com/88224293/167246371-b5134158-271f-48cd-bb05-176e829cb843.png)
>http://www.multi.k.u-tokyo.ac.jp/lectures/H18_HPC/materials/FEM_2D.PDF

### アイソパラメトリック要素




![\begin{align}
\text{node}          & & \text{node i} & & \text{node j} & & \text{node k} & & \text{node l} \\
\text{coordinate(\xi,\eta)} & & (-1,-1) & & (1,-1) & & (1,1) & & (-1,1)
\end{align}](https://render.githubusercontent.com/render/math?math=%5Ccolor%7Bblack%7D%5Cdisplaystyle+%5Cbegin%7Balign%7D%0A%5Ctext%7Bnode%7D++++++++++%26+%26+%5Ctext%7Bnode+i%7D+%26+%26+%5Ctext%7Bnode+j%7D+%26+%26+%5Ctext%7Bnode+k%7D+%26+%26+%5Ctext%7Bnode+l%7D+%5C%5C%0A%5Ctext%7Bcoordinate%28%5Cxi%2C%5Ceta%29%7D+%26+%26+%28-1%2C-1%29+%26+%26+%281%2C-1%29+%26+%26+%281%2C1%29+%26+%26+%28-1%2C1%29%0A%5Cend%7Balign%7D)






![\begin{align}
N_1=\frac{1}{4}(1-\xi)(1-\eta) \qquad  N_2=\frac{1}{4}(1+\xi)(1-\eta) \\
N_3=\frac{1}{4}(1+\xi)(1+\eta) \qquad N_4=\frac{1}{4}(1-\xi)(1+\eta)
\end{align}](https://render.githubusercontent.com/render/math?math=%5Ccolor%7Bblack%7D%5Cdisplaystyle+%5Cbegin%7Balign%7D%0AN_1%3D%5Cfrac%7B1%7D%7B4%7D%281-%5Cxi%29%281-%5Ceta%29+%5Cqquad++N_2%3D%5Cfrac%7B1%7D%7B4%7D%281%2B%5Cxi%29%281-%5Ceta%29+%5C%5C%0AN_3%3D%5Cfrac%7B1%7D%7B4%7D%281%2B%5Cxi%29%281%2B%5Ceta%29+%5Cqquad+N_4%3D%5Cfrac%7B1%7D%7B4%7D%281-%5Cxi%29%281%2B%5Ceta%29%0A%5Cend%7Balign%7D)






![\begin{align}
&\cfrac{\partial N_1}{\partial \xi}=-\cfrac{1}{4}(1-\eta)  &&\cfrac{\partial N_2}{\partial \xi}=+\cfrac{1}{4}(1-\eta) & &\cfrac{\partial N_3}{\partial \xi}=+\cfrac{1}{4}(1+\eta) & &\cfrac{\partial N_4}{\partial \xi}=-\cfrac{1}{4}(1+\eta) \\
&\cfrac{\partial N_1}{\partial \eta}=-\cfrac{1}{4}(1-\xi)  &&\cfrac{\partial N_2}{\partial \eta}=-\cfrac{1}{4}(1+\xi) & &\cfrac{\partial N_3}{\partial \eta}=+\cfrac{1}{4}(1+\xi) & &\cfrac{\partial N_4}{\partial \eta}=+\cfrac{1}{4}(1-\xi)
\end{align}](https://render.githubusercontent.com/render/math?math=%5Ccolor%7Bblack%7D%5Cdisplaystyle+%5Cbegin%7Balign%7D%0A%26%5Ccfrac%7B%5Cpartial+N_1%7D%7B%5Cpartial+%5Cxi%7D%3D-%5Ccfrac%7B1%7D%7B4%7D%281-%5Ceta%29++%26%26%5Ccfrac%7B%5Cpartial+N_2%7D%7B%5Cpartial+%5Cxi%7D%3D%2B%5Ccfrac%7B1%7D%7B4%7D%281-%5Ceta%29+%26+%26%5Ccfrac%7B%5Cpartial+N_3%7D%7B%5Cpartial+%5Cxi%7D%3D%2B%5Ccfrac%7B1%7D%7B4%7D%281%2B%5Ceta%29+%26+%26%5Ccfrac%7B%5Cpartial+N_4%7D%7B%5Cpartial+%5Cxi%7D%3D-%5Ccfrac%7B1%7D%7B4%7D%281%2B%5Ceta%29+%5C%5C%0A%26%5Ccfrac%7B%5Cpartial+N_1%7D%7B%5Cpartial+%5Ceta%7D%3D-%5Ccfrac%7B1%7D%7B4%7D%281-%5Cxi%29++%26%26%5Ccfrac%7B%5Cpartial+N_2%7D%7B%5Cpartial+%5Ceta%7D%3D-%5Ccfrac%7B1%7D%7B4%7D%281%2B%5Cxi%29+%26+%26%5Ccfrac%7B%5Cpartial+N_3%7D%7B%5Cpartial+%5Ceta%7D%3D%2B%5Ccfrac%7B1%7D%7B4%7D%281%2B%5Cxi%29+%26+%26%5Ccfrac%7B%5Cpartial+N_4%7D%7B%5Cpartial+%5Ceta%7D%3D%2B%5Ccfrac%7B1%7D%7B4%7D%281-%5Cxi%29%0A%5Cend%7Balign%7D)




![\begin{equation}
\{\boldsymbol{d}\}=\begin{Bmatrix} u \\ v  \end{Bmatrix}
=\begin{bmatrix}
N_1 & N_2 & N_3 & N_4    \\
\end{bmatrix}
\begin{Bmatrix}
u_1 & v_1 \\ 
u_2 & v_2 \\ 
u_3 & v_3 \\
u_4 & v_4
\end{Bmatrix}\\
=\begin{bmatrix}
N_1 & 0 & N_2 & 0 & N_3 & 0 & N_4 & 0    \\
0 & N_1 & 0 & N_2 & 0 & N_3 & 0 & N_4    \\
\end{bmatrix}
\begin{Bmatrix}
u_1 \\ v_1 \\ 
u_2 \\ v_2 \\ 
u_3 \\ v_3 \\
u_4 \\  v_4
\end{Bmatrix}\\
=[\boldsymbol{N}]\{\boldsymbol{d}\}
\end{equation}](https://render.githubusercontent.com/render/math?math=%5Ccolor%7Bblack%7D%5Cdisplaystyle+%5Cbegin%7Bequation%7D%0A%5C%7B%5Cboldsymbol%7Bd%7D%5C%7D%3D%5Cbegin%7BBmatrix%7D+u+%5C%5C+v++%5Cend%7BBmatrix%7D%0A%3D%5Cbegin%7Bbmatrix%7D%0AN_1+%26+N_2+%26+N_3+%26+N_4++++%5C%5C%0A%5Cend%7Bbmatrix%7D%0A%5Cbegin%7BBmatrix%7D%0Au_1+%26+v_1+%5C%5C+%0Au_2+%26+v_2+%5C%5C+%0Au_3+%26+v_3+%5C%5C%0Au_4+%26+v_4%0A%5Cend%7BBmatrix%7D%5C%5C%0A%3D%5Cbegin%7Bbmatrix%7D%0AN_1+%26+0+%26+N_2+%26+0+%26+N_3+%26+0+%26+N_4+%26+0++++%5C%5C%0A0+%26+N_1+%26+0+%26+N_2+%26+0+%26+N_3+%26+0+%26+N_4++++%5C%5C%0A%5Cend%7Bbmatrix%7D%0A%5Cbegin%7BBmatrix%7D%0Au_1+%5C%5C+v_1+%5C%5C+%0Au_2+%5C%5C+v_2+%5C%5C+%0Au_3+%5C%5C+v_3+%5C%5C%0Au_4+%5C%5C++v_4%0A%5Cend%7BBmatrix%7D%5C%5C%0A%3D%5B%5Cboldsymbol%7BN%7D%5D%5C%7B%5Cboldsymbol%7Bd%7D%5C%7D%0A%5Cend%7Bequation%7D)




![\begin{equation}
\boldsymbol{H}(\xi=ga, \eta=ga)
=\left. \begin{bmatrix}
\frac{\partial N_1}{\partial \xi} & \frac{\partial N_2}{\partial \xi} & \frac{\partial N_3}{\partial \xi} &\frac{\partial N_4}{\partial \xi}\\
\frac{\partial N_1}{\partial \eta}  & \frac{\partial N_2}{\partial \eta} & \frac{\partial N_3}{\partial \eta} &\frac{\partial N_4}{\partial \eta}\\
\end{bmatrix}\right|_{(\xi, \eta)=(ga,ga)}
\end{equation}](https://render.githubusercontent.com/render/math?math=%5Ccolor%7Bblack%7D%5Cdisplaystyle+%5Cbegin%7Bequation%7D%0A%5Cboldsymbol%7BH%7D%28%5Cxi%3Dga%2C+%5Ceta%3Dga%29%0A%3D%5Cleft.+%5Cbegin%7Bbmatrix%7D%0A%5Cfrac%7B%5Cpartial+N_1%7D%7B%5Cpartial+%5Cxi%7D+%26+%5Cfrac%7B%5Cpartial+N_2%7D%7B%5Cpartial+%5Cxi%7D+%26+%5Cfrac%7B%5Cpartial+N_3%7D%7B%5Cpartial+%5Cxi%7D+%26%5Cfrac%7B%5Cpartial+N_4%7D%7B%5Cpartial+%5Cxi%7D%5C%5C%0A%5Cfrac%7B%5Cpartial+N_1%7D%7B%5Cpartial+%5Ceta%7D++%26+%5Cfrac%7B%5Cpartial+N_2%7D%7B%5Cpartial+%5Ceta%7D+%26+%5Cfrac%7B%5Cpartial+N_3%7D%7B%5Cpartial+%5Ceta%7D+%26%5Cfrac%7B%5Cpartial+N_4%7D%7B%5Cpartial+%5Ceta%7D%5C%5C%0A%5Cend%7Bbmatrix%7D%5Cright%7C_%7B%28%5Cxi%2C+%5Ceta%29%3D%28ga%2Cga%29%7D%0A%5Cend%7Bequation%7D)



![\begin{equation}
\{e\_node\}
= \begin{bmatrix}
x_1 & y_1\\
x_2 & y_2\\
x_3 & y_3\\
x_4 & y_4\\
\end{bmatrix}
\end{equation}](https://render.githubusercontent.com/render/math?math=%5Ccolor%7Bblack%7D%5Cdisplaystyle+%5Cbegin%7Bequation%7D%0A%5C%7Be%5C_node%5C%7D%0A%3D+%5Cbegin%7Bbmatrix%7D%0Ax_1+%26+y_1%5C%5C%0Ax_2+%26+y_2%5C%5C%0Ax_3+%26+y_3%5C%5C%0Ax_4+%26+y_4%5C%5C%0A%5Cend%7Bbmatrix%7D%0A%5Cend%7Bequation%7D)




![\begin{equation}
\boldsymbol{J}(\xi=ga, \eta=ga)
=\left. \begin{bmatrix}
\frac{\partial x}{\partial \xi}  &\frac{\partial y}{\partial \xi}  \\
\frac{\partial x}{\partial \eta}  &\frac{\partial y}{\partial \eta}\\
\end{bmatrix}\right| _{(\xi, \eta)=(ga,ga)}  \\
=\left. \begin{bmatrix}
\frac{\partial N_1}{\partial \xi} & \frac{\partial N_2}{\partial \xi} & \frac{\partial N_3}{\partial \xi} &\frac{\partial N_4}{\partial \xi}\\
\frac{\partial N_1}{\partial \eta}  & \frac{\partial N_2}{\partial \eta} & \frac{\partial N_3}{\partial \eta} &\frac{\partial N_4}{\partial \eta}\\
\end{bmatrix}\right|_{(\xi, \eta)=(ga,ga)}
\begin{bmatrix}
x_1 & y_1\\
x_2 & y_2\\
x_3 & y_3\\
x_4 & y_4\\
\end{bmatrix}
=\boldsymbol{H}_{(\xi=ga, \eta=ga)} \{ e\_node\}
\end{equation}](https://render.githubusercontent.com/render/math?math=%5Ccolor%7Bblack%7D%5Cdisplaystyle+%5Cbegin%7Bequation%7D%0A%5Cboldsymbol%7BJ%7D%28%5Cxi%3Dga%2C+%5Ceta%3Dga%29%0A%3D%5Cleft.+%5Cbegin%7Bbmatrix%7D%0A%5Cfrac%7B%5Cpartial+x%7D%7B%5Cpartial+%5Cxi%7D++%26%5Cfrac%7B%5Cpartial+y%7D%7B%5Cpartial+%5Cxi%7D++%5C%5C%0A%5Cfrac%7B%5Cpartial+x%7D%7B%5Cpartial+%5Ceta%7D++%26%5Cfrac%7B%5Cpartial+y%7D%7B%5Cpartial+%5Ceta%7D%5C%5C%0A%5Cend%7Bbmatrix%7D%5Cright%7C+_%7B%28%5Cxi%2C+%5Ceta%29%3D%28ga%2Cga%29%7D++%5C%5C%0A%3D%5Cleft.+%5Cbegin%7Bbmatrix%7D%0A%5Cfrac%7B%5Cpartial+N_1%7D%7B%5Cpartial+%5Cxi%7D+%26+%5Cfrac%7B%5Cpartial+N_2%7D%7B%5Cpartial+%5Cxi%7D+%26+%5Cfrac%7B%5Cpartial+N_3%7D%7B%5Cpartial+%5Cxi%7D+%26%5Cfrac%7B%5Cpartial+N_4%7D%7B%5Cpartial+%5Cxi%7D%5C%5C%0A%5Cfrac%7B%5Cpartial+N_1%7D%7B%5Cpartial+%5Ceta%7D++%26+%5Cfrac%7B%5Cpartial+N_2%7D%7B%5Cpartial+%5Ceta%7D+%26+%5Cfrac%7B%5Cpartial+N_3%7D%7B%5Cpartial+%5Ceta%7D+%26%5Cfrac%7B%5Cpartial+N_4%7D%7B%5Cpartial+%5Ceta%7D%5C%5C%0A%5Cend%7Bbmatrix%7D%5Cright%7C_%7B%28%5Cxi%2C+%5Ceta%29%3D%28ga%2Cga%29%7D%0A%5Cbegin%7Bbmatrix%7D%0Ax_1+%26+y_1%5C%5C%0Ax_2+%26+y_2%5C%5C%0Ax_3+%26+y_3%5C%5C%0Ax_4+%26+y_4%5C%5C%0A%5Cend%7Bbmatrix%7D%0A%3D%5Cboldsymbol%7BH%7D_%7B%28%5Cxi%3Dga%2C+%5Ceta%3Dga%29%7D+%5C%7B+e%5C_node%5C%7D%0A%5Cend%7Bequation%7D)














![\begin{equation}
\{dNdxy\} =
\left. \begin{bmatrix}
\frac{\partial N_1}{\partial x} & \frac{\partial N_2}{\partial x} & \frac{\partial N_3}{\partial x} &\frac{\partial N_4}{\partial x}\\
\frac{\partial N_1}{\partial y}  & \frac{\partial N_2}{\partial y} & \frac{\partial N_3}{\partial y} &\frac{\partial N_4}{\partial y}\\
\end{bmatrix}\right|_{(\xi, \eta)=(ga,ga)}
\\
=\left. \begin{bmatrix}
\frac{\partial N_1}{\partial \xi} \frac{\partial \xi}{\partial x}  + \frac{\partial N_1}{\partial \eta}  \frac{\partial \eta}{\partial x}  
& \frac{\partial N_2}{\partial \xi} \frac{\partial \xi}{\partial x}  + \frac{\partial N_2}{\partial \eta}  \frac{\partial \eta}{\partial x}  
& \frac{\partial N_3}{\partial \xi} \frac{\partial \xi}{\partial x}  + \frac{\partial N_3}{\partial \eta}  \frac{\partial \eta}{\partial x}  
&\frac{\partial N_4}{\partial \xi} \frac{\partial \xi}{\partial x} + \frac{\partial N_4}{\partial \eta}  \frac{\partial \eta}{\partial x} 
 \\
\frac{\partial N_1}{\partial \xi} \frac{\partial \xi}{\partial y}  + \frac{\partial N_1}{\partial \eta}  \frac{\partial \eta}{\partial y}  
& \frac{\partial N_2}{\partial \xi} \frac{\partial \xi}{\partial y}  + \frac{\partial N_2}{\partial \eta}  \frac{\partial \eta}{\partial y}  
& \frac{\partial N_3}{\partial \xi} \frac{\partial \xi}{\partial y}  + \frac{\partial N_3}{\partial \eta}  \frac{\partial \eta}{\partial y}  
&\frac{\partial N_4}{\partial \xi} \frac{\partial \xi}{\partial y} + \frac{\partial N_4}{\partial \eta}  \frac{\partial \eta}{\partial y}  \\
\end{bmatrix}\right|_{(\xi, \eta)=(ga,ga)}
\\
=\left. \begin{bmatrix}
\frac{\partial \xi}{\partial x}  &\frac{\partial \eta}{\partial x}  \\
\frac{\partial \eta}{\partial y}  &\frac{\partial \eta}{\partial y}\\
\end{bmatrix}\right| _{(\xi, \eta)=(ga,ga)} 
\left. \begin{bmatrix}
\frac{\partial N_1}{\partial \xi} & \frac{\partial N_2}{\partial \xi} & \frac{\partial N_3}{\partial \xi} &\frac{\partial N_4}{\partial \xi}\\
\frac{\partial N_1}{\partial \eta}  & \frac{\partial N_2}{\partial \eta} & \frac{\partial N_3}{\partial \eta} &\frac{\partial N_4}{\partial \eta}\\
\end{bmatrix}\right|_{(\xi, \eta)=(ga,ga)}
\\
=\left. \begin{bmatrix}
\frac{\partial x}{\partial \xi}  &\frac{\partial y}{\partial \xi}  \\
\frac{\partial x}{\partial \eta}  &\frac{\partial y}{\partial \eta}\\
\end{bmatrix}^{-1}\right| _{(\xi, \eta)=(ga,ga)} 
\left. \begin{bmatrix}
\frac{\partial N_1}{\partial \xi} & \frac{\partial N_2}{\partial \xi} & \frac{\partial N_3}{\partial \xi} &\frac{\partial N_4}{\partial \xi}\\
\frac{\partial N_1}{\partial \eta}  & \frac{\partial N_2}{\partial \eta} & \frac{\partial N_3}{\partial \eta} &\frac{\partial N_4}{\partial \eta}\\
\end{bmatrix}\right|_{(\xi, \eta)=(ga,ga)}
\\
=\boldsymbol{J}^{-1}(\xi=ga, \eta=ga)\boldsymbol{H}(\xi=ga, \eta=ga)
\end{equation}](https://render.githubusercontent.com/render/math?math=%5Ccolor%7Bblack%7D%5Cdisplaystyle+%5Cbegin%7Bequation%7D%0A%5C%7BdNdxy%5C%7D+%3D%0A%5Cleft.+%5Cbegin%7Bbmatrix%7D%0A%5Cfrac%7B%5Cpartial+N_1%7D%7B%5Cpartial+x%7D+%26+%5Cfrac%7B%5Cpartial+N_2%7D%7B%5Cpartial+x%7D+%26+%5Cfrac%7B%5Cpartial+N_3%7D%7B%5Cpartial+x%7D+%26%5Cfrac%7B%5Cpartial+N_4%7D%7B%5Cpartial+x%7D%5C%5C%0A%5Cfrac%7B%5Cpartial+N_1%7D%7B%5Cpartial+y%7D++%26+%5Cfrac%7B%5Cpartial+N_2%7D%7B%5Cpartial+y%7D+%26+%5Cfrac%7B%5Cpartial+N_3%7D%7B%5Cpartial+y%7D+%26%5Cfrac%7B%5Cpartial+N_4%7D%7B%5Cpartial+y%7D%5C%5C%0A%5Cend%7Bbmatrix%7D%5Cright%7C_%7B%28%5Cxi%2C+%5Ceta%29%3D%28ga%2Cga%29%7D%0A%5C%5C%0A%3D%5Cleft.+%5Cbegin%7Bbmatrix%7D%0A%5Cfrac%7B%5Cpartial+N_1%7D%7B%5Cpartial+%5Cxi%7D+%5Cfrac%7B%5Cpartial+%5Cxi%7D%7B%5Cpartial+x%7D++%2B+%5Cfrac%7B%5Cpartial+N_1%7D%7B%5Cpartial+%5Ceta%7D++%5Cfrac%7B%5Cpartial+%5Ceta%7D%7B%5Cpartial+x%7D++%0A%26+%5Cfrac%7B%5Cpartial+N_2%7D%7B%5Cpartial+%5Cxi%7D+%5Cfrac%7B%5Cpartial+%5Cxi%7D%7B%5Cpartial+x%7D++%2B+%5Cfrac%7B%5Cpartial+N_2%7D%7B%5Cpartial+%5Ceta%7D++%5Cfrac%7B%5Cpartial+%5Ceta%7D%7B%5Cpartial+x%7D++%0A%26+%5Cfrac%7B%5Cpartial+N_3%7D%7B%5Cpartial+%5Cxi%7D+%5Cfrac%7B%5Cpartial+%5Cxi%7D%7B%5Cpartial+x%7D++%2B+%5Cfrac%7B%5Cpartial+N_3%7D%7B%5Cpartial+%5Ceta%7D++%5Cfrac%7B%5Cpartial+%5Ceta%7D%7B%5Cpartial+x%7D++%0A%26%5Cfrac%7B%5Cpartial+N_4%7D%7B%5Cpartial+%5Cxi%7D+%5Cfrac%7B%5Cpartial+%5Cxi%7D%7B%5Cpartial+x%7D+%2B+%5Cfrac%7B%5Cpartial+N_4%7D%7B%5Cpartial+%5Ceta%7D++%5Cfrac%7B%5Cpartial+%5Ceta%7D%7B%5Cpartial+x%7D+%0A+%5C%5C%0A%5Cfrac%7B%5Cpartial+N_1%7D%7B%5Cpartial+%5Cxi%7D+%5Cfrac%7B%5Cpartial+%5Cxi%7D%7B%5Cpartial+y%7D++%2B+%5Cfrac%7B%5Cpartial+N_1%7D%7B%5Cpartial+%5Ceta%7D++%5Cfrac%7B%5Cpartial+%5Ceta%7D%7B%5Cpartial+y%7D++%0A%26+%5Cfrac%7B%5Cpartial+N_2%7D%7B%5Cpartial+%5Cxi%7D+%5Cfrac%7B%5Cpartial+%5Cxi%7D%7B%5Cpartial+y%7D++%2B+%5Cfrac%7B%5Cpartial+N_2%7D%7B%5Cpartial+%5Ceta%7D++%5Cfrac%7B%5Cpartial+%5Ceta%7D%7B%5Cpartial+y%7D++%0A%26+%5Cfrac%7B%5Cpartial+N_3%7D%7B%5Cpartial+%5Cxi%7D+%5Cfrac%7B%5Cpartial+%5Cxi%7D%7B%5Cpartial+y%7D++%2B+%5Cfrac%7B%5Cpartial+N_3%7D%7B%5Cpartial+%5Ceta%7D++%5Cfrac%7B%5Cpartial+%5Ceta%7D%7B%5Cpartial+y%7D++%0A%26%5Cfrac%7B%5Cpartial+N_4%7D%7B%5Cpartial+%5Cxi%7D+%5Cfrac%7B%5Cpartial+%5Cxi%7D%7B%5Cpartial+y%7D+%2B+%5Cfrac%7B%5Cpartial+N_4%7D%7B%5Cpartial+%5Ceta%7D++%5Cfrac%7B%5Cpartial+%5Ceta%7D%7B%5Cpartial+y%7D++%5C%5C%0A%5Cend%7Bbmatrix%7D%5Cright%7C_%7B%28%5Cxi%2C+%5Ceta%29%3D%28ga%2Cga%29%7D%0A%5C%5C%0A%3D%5Cleft.+%5Cbegin%7Bbmatrix%7D%0A%5Cfrac%7B%5Cpartial+%5Cxi%7D%7B%5Cpartial+x%7D++%26%5Cfrac%7B%5Cpartial+%5Ceta%7D%7B%5Cpartial+x%7D++%5C%5C%0A%5Cfrac%7B%5Cpartial+%5Ceta%7D%7B%5Cpartial+y%7D++%26%5Cfrac%7B%5Cpartial+%5Ceta%7D%7B%5Cpartial+y%7D%5C%5C%0A%5Cend%7Bbmatrix%7D%5Cright%7C+_%7B%28%5Cxi%2C+%5Ceta%29%3D%28ga%2Cga%29%7D+%0A%5Cleft.+%5Cbegin%7Bbmatrix%7D%0A%5Cfrac%7B%5Cpartial+N_1%7D%7B%5Cpartial+%5Cxi%7D+%26+%5Cfrac%7B%5Cpartial+N_2%7D%7B%5Cpartial+%5Cxi%7D+%26+%5Cfrac%7B%5Cpartial+N_3%7D%7B%5Cpartial+%5Cxi%7D+%26%5Cfrac%7B%5Cpartial+N_4%7D%7B%5Cpartial+%5Cxi%7D%5C%5C%0A%5Cfrac%7B%5Cpartial+N_1%7D%7B%5Cpartial+%5Ceta%7D++%26+%5Cfrac%7B%5Cpartial+N_2%7D%7B%5Cpartial+%5Ceta%7D+%26+%5Cfrac%7B%5Cpartial+N_3%7D%7B%5Cpartial+%5Ceta%7D+%26%5Cfrac%7B%5Cpartial+N_4%7D%7B%5Cpartial+%5Ceta%7D%5C%5C%0A%5Cend%7Bbmatrix%7D%5Cright%7C_%7B%28%5Cxi%2C+%5Ceta%29%3D%28ga%2Cga%29%7D%0A%5C%5C%0A%3D%5Cleft.+%5Cbegin%7Bbmatrix%7D%0A%5Cfrac%7B%5Cpartial+x%7D%7B%5Cpartial+%5Cxi%7D++%26%5Cfrac%7B%5Cpartial+y%7D%7B%5Cpartial+%5Cxi%7D++%5C%5C%0A%5Cfrac%7B%5Cpartial+x%7D%7B%5Cpartial+%5Ceta%7D++%26%5Cfrac%7B%5Cpartial+y%7D%7B%5Cpartial+%5Ceta%7D%5C%5C%0A%5Cend%7Bbmatrix%7D%5E%7B-1%7D%5Cright%7C+_%7B%28%5Cxi%2C+%5Ceta%29%3D%28ga%2Cga%29%7D+%0A%5Cleft.+%5Cbegin%7Bbmatrix%7D%0A%5Cfrac%7B%5Cpartial+N_1%7D%7B%5Cpartial+%5Cxi%7D+%26+%5Cfrac%7B%5Cpartial+N_2%7D%7B%5Cpartial+%5Cxi%7D+%26+%5Cfrac%7B%5Cpartial+N_3%7D%7B%5Cpartial+%5Cxi%7D+%26%5Cfrac%7B%5Cpartial+N_4%7D%7B%5Cpartial+%5Cxi%7D%5C%5C%0A%5Cfrac%7B%5Cpartial+N_1%7D%7B%5Cpartial+%5Ceta%7D++%26+%5Cfrac%7B%5Cpartial+N_2%7D%7B%5Cpartial+%5Ceta%7D+%26+%5Cfrac%7B%5Cpartial+N_3%7D%7B%5Cpartial+%5Ceta%7D+%26%5Cfrac%7B%5Cpartial+N_4%7D%7B%5Cpartial+%5Ceta%7D%5C%5C%0A%5Cend%7Bbmatrix%7D%5Cright%7C_%7B%28%5Cxi%2C+%5Ceta%29%3D%28ga%2Cga%29%7D%0A%5C%5C%0A%3D%5Cboldsymbol%7BJ%7D%5E%7B-1%7D%28%5Cxi%3Dga%2C+%5Ceta%3Dga%29%5Cboldsymbol%7BH%7D%28%5Cxi%3Dga%2C+%5Ceta%3Dga%29%0A%5Cend%7Bequation%7D)

















![\begin{equation}
\{\boldsymbol{\epsilon}\}=\begin{Bmatrix} \cfrac{\partial u}{\partial x} \\ \cfrac{\partial v}{\partial y} \\ \cfrac{\partial u}{\partial y}+\cfrac{\partial v}{\partial x} \end{Bmatrix}
=\begin{bmatrix}
\cfrac{\partial N_1}{\partial x} & 0 & \cfrac{\partial N_2}{\partial x} & 0 & \cfrac{\partial N_3}{\partial x} & 0 & \cfrac{\partial N_4}{\partial x} & 0 \\
0 & \cfrac{\partial N_1}{\partial y} & 0 & \cfrac{\partial N_2}{\partial y} & 0 & \cfrac{\partial N_3}{\partial y} & 0 & \cfrac{\partial N_4}{\partial y} \\
\cfrac{\partial N_1}{\partial y} & \cfrac{\partial N_1}{\partial x} & \cfrac{\partial N_2}{\partial y} & \cfrac{\partial N_2}{\partial x} & \cfrac{\partial N_3}{\partial y} & \cfrac{\partial N_3}{\partial x} & \cfrac{\partial N_4}{\partial y} & \cfrac{\partial N_4}{\partial x}
\end{bmatrix}
\begin{Bmatrix}
u_i \\ v_i \\ u_j \\ v_j \\ u_k \\ v_k \\ u_l \\ v_l
\end{Bmatrix}
=[\boldsymbol{B}]\{\boldsymbol{u_{nd}}\}
\end{equation}](https://render.githubusercontent.com/render/math?math=%5Ccolor%7Bblack%7D%5Cdisplaystyle+%5Cbegin%7Bequation%7D%0A%5C%7B%5Cboldsymbol%7B%5Cepsilon%7D%5C%7D%3D%5Cbegin%7BBmatrix%7D+%5Ccfrac%7B%5Cpartial+u%7D%7B%5Cpartial+x%7D+%5C%5C+%5Ccfrac%7B%5Cpartial+v%7D%7B%5Cpartial+y%7D+%5C%5C+%5Ccfrac%7B%5Cpartial+u%7D%7B%5Cpartial+y%7D%2B%5Ccfrac%7B%5Cpartial+v%7D%7B%5Cpartial+x%7D+%5Cend%7BBmatrix%7D%0A%3D%5Cbegin%7Bbmatrix%7D%0A%5Ccfrac%7B%5Cpartial+N_1%7D%7B%5Cpartial+x%7D+%26+0+%26+%5Ccfrac%7B%5Cpartial+N_2%7D%7B%5Cpartial+x%7D+%26+0+%26+%5Ccfrac%7B%5Cpartial+N_3%7D%7B%5Cpartial+x%7D+%26+0+%26+%5Ccfrac%7B%5Cpartial+N_4%7D%7B%5Cpartial+x%7D+%26+0+%5C%5C%0A0+%26+%5Ccfrac%7B%5Cpartial+N_1%7D%7B%5Cpartial+y%7D+%26+0+%26+%5Ccfrac%7B%5Cpartial+N_2%7D%7B%5Cpartial+y%7D+%26+0+%26+%5Ccfrac%7B%5Cpartial+N_3%7D%7B%5Cpartial+y%7D+%26+0+%26+%5Ccfrac%7B%5Cpartial+N_4%7D%7B%5Cpartial+y%7D+%5C%5C%0A%5Ccfrac%7B%5Cpartial+N_1%7D%7B%5Cpartial+y%7D+%26+%5Ccfrac%7B%5Cpartial+N_1%7D%7B%5Cpartial+x%7D+%26+%5Ccfrac%7B%5Cpartial+N_2%7D%7B%5Cpartial+y%7D+%26+%5Ccfrac%7B%5Cpartial+N_2%7D%7B%5Cpartial+x%7D+%26+%5Ccfrac%7B%5Cpartial+N_3%7D%7B%5Cpartial+y%7D+%26+%5Ccfrac%7B%5Cpartial+N_3%7D%7B%5Cpartial+x%7D+%26+%5Ccfrac%7B%5Cpartial+N_4%7D%7B%5Cpartial+y%7D+%26+%5Ccfrac%7B%5Cpartial+N_4%7D%7B%5Cpartial+x%7D%0A%5Cend%7Bbmatrix%7D%0A%5Cbegin%7BBmatrix%7D%0Au_i+%5C%5C+v_i+%5C%5C+u_j+%5C%5C+v_j+%5C%5C+u_k+%5C%5C+v_k+%5C%5C+u_l+%5C%5C+v_l%0A%5Cend%7BBmatrix%7D%0A%3D%5B%5Cboldsymbol%7BB%7D%5D%5C%7B%5Cboldsymbol%7Bu_%7Bnd%7D%7D%5C%7D%0A%5Cend%7Bequation%7D)








## Kmat




### ガウス・ルジャンドル数値積分

https://qiita.com/yuki_2020/items/1ba48481b930fc3998fc

各積分点の値を足すことで要素内で積分をしている。





![\begin{align}
[\boldsymbol{K_e}]=\int_A[\boldsymbol{B_e}]^T[\boldsymbol{D_e}][\boldsymbol{B_e}]hdA
=h \int_{-1}^1 \int_{-1}^1  [\boldsymbol{B_e}]^T[\boldsymbol{D_e}][\boldsymbol{B_e}]
det(\boldsymbol{J}(\xi,\eta)) 
d \xi d \eta \\
= \sum_{i=1}^n \sum_{j=1}^n w_i w_j  [\boldsymbol{B_e}]^T(\xi_i,\eta_j)[\boldsymbol{D_e}][\boldsymbol{B_e}](\xi_i,\eta_j) det(\boldsymbol{J}(\xi_i,\eta_j)) \\
= \sum_{i=1}^2 \sum_{j=1}^2 1 \cdot 1  [\boldsymbol{B_e}]^T(\xi_i,\eta_j)[\boldsymbol{D_e}][\boldsymbol{B_e}](\xi_i,\eta_j) det(\boldsymbol{J}(\xi_i,\eta_j)) 
\end{align}](https://render.githubusercontent.com/render/math?math=%5Ccolor%7Bblack%7D%5Cdisplaystyle+%5Cbegin%7Balign%7D%0A%5B%5Cboldsymbol%7BK_e%7D%5D%3D%5Cint_A%5B%5Cboldsymbol%7BB_e%7D%5D%5ET%5B%5Cboldsymbol%7BD_e%7D%5D%5B%5Cboldsymbol%7BB_e%7D%5DhdA%0A%3Dh+%5Cint_%7B-1%7D%5E1+%5Cint_%7B-1%7D%5E1++%5B%5Cboldsymbol%7BB_e%7D%5D%5ET%5B%5Cboldsymbol%7BD_e%7D%5D%5B%5Cboldsymbol%7BB_e%7D%5D%0Adet%28%5Cboldsymbol%7BJ%7D%28%5Cxi%2C%5Ceta%29%29+%0Ad+%5Cxi+d+%5Ceta+%5C%5C%0A%3D+%5Csum_%7Bi%3D1%7D%5En+%5Csum_%7Bj%3D1%7D%5En+w_i+w_j++%5B%5Cboldsymbol%7BB_e%7D%5D%5ET%28%5Cxi_i%2C%5Ceta_j%29%5B%5Cboldsymbol%7BD_e%7D%5D%5B%5Cboldsymbol%7BB_e%7D%5D%28%5Cxi_i%2C%5Ceta_j%29+det%28%5Cboldsymbol%7BJ%7D%28%5Cxi_i%2C%5Ceta_j%29%29+%5C%5C%0A%3D+%5Csum_%7Bi%3D1%7D%5E2+%5Csum_%7Bj%3D1%7D%5E2+1+%5Ccdot+1++%5B%5Cboldsymbol%7BB_e%7D%5D%5ET%28%5Cxi_i%2C%5Ceta_j%29%5B%5Cboldsymbol%7BD_e%7D%5D%5B%5Cboldsymbol%7BB_e%7D%5D%28%5Cxi_i%2C%5Ceta_j%29+det%28%5Cboldsymbol%7BJ%7D%28%5Cxi_i%2C%5Ceta_j%29%29+%0A%5Cend%7Balign%7D)










## distribution


三角形要素では要素内のひずみ、応力は一定であった。
しかし、四角形要素では一定ではなく、要素内で分布がある。

今回、ひずみ、応力ともにガウスの積分点における値はすぐに計算することができる。
それをプログラムでは`GAUSSstrain`、`GAUSSstress`と呼んでいる。



`NODALstrain` 、`NODALstress`は節点での値。
積分点での値が正確なので、そこから求める。

変位場は形状関数で仮定していたが、ひずみ、応力についても同様の変位場を仮定する。
積分点での値はわかっているので、節点での値は連立方程式を解くことで分かる。


![\begin{equation}
 \left. \begin{bmatrix}
N_1 & N_2 & N_3 & N_4    \\
\end{bmatrix}\right|_{(\xi=ga, \eta = ga)}
\begin{Bmatrix} \epsilon_{x1} \\ \epsilon_{x2} \\\epsilon_{x3} \\ \epsilon_{x4}  \end{Bmatrix}
= \epsilon(ga)
\end{equation}](https://render.githubusercontent.com/render/math?math=%5Ccolor%7Bblack%7D%5Cdisplaystyle+%5Cbegin%7Bequation%7D%0A+%5Cleft.+%5Cbegin%7Bbmatrix%7D%0AN_1+%26+N_2+%26+N_3+%26+N_4++++%5C%5C%0A%5Cend%7Bbmatrix%7D%5Cright%7C_%7B%28%5Cxi%3Dga%2C+%5Ceta+%3D+ga%29%7D%0A%5Cbegin%7BBmatrix%7D+%5Cepsilon_%7Bx1%7D+%5C%5C+%5Cepsilon_%7Bx2%7D+%5C%5C%5Cepsilon_%7Bx3%7D+%5C%5C+%5Cepsilon_%7Bx4%7D++%5Cend%7BBmatrix%7D%0A%3D+%5Cepsilon%28ga%29%0A%5Cend%7Bequation%7D)







# Version1.0.1

# 変更点
バグの修正
#7

## What's Changed
* e_Kmatの初期化位置を変更 by @yuki-2000 in https://github.com/yuki-2000/2D4Node_FEM/pull/8


**Full Changelog**: https://github.com/yuki-2000/2D4Node_FEM/compare/v1.0.0...v1.0.1







# Version 1.1.0

# 平均応力、ひずみを追加、det_Jacobi修正
可視化でも平均を使用するように変更

# ヤコビアンが負になったときにエラー出力
https://github.com/yuki-2000/2D4Node_FEM/issues/9

# モデル一新、メッシュをより見やすく
モデル
2000 !モデル節点数
1881 !モデル要素数
1 !材料種類数
40 !拘束点数
の片持ち梁に変更。
それに伴って荷重なども変更

メッシュ
すべてのメッシュが変形前、ある値分布になっていたので、変形後、それぞれの値に修正
メッシュの点が大きすぎたので削除
メッシュの線が太すぎたので`,linewidths=(0.1,)`に変更
グラフの解像度を`dpi=500`に
軸の名前の変更


## What's Changed
* Update by @yuki-2000 in https://github.com/yuki-2000/2D4Node_FEM/pull/11


**Full Changelog**: https://github.com/yuki-2000/2D4Node_FEM/compare/v1.0.1...v1.1.0
