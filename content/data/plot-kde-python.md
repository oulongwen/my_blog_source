Title: How to Plot Probability Density Function (PDF) in Python
Date: 2017-01-19 23:44
Tags: Python, pandas, matplotlib
Slug: python-pdf
Author: Longwen Ou
Summary: Plotting probability density function with python

In my research I often want to plot the Probability Density Function (PDF) of simulation data. It is pretty straightforward to plot a Cumulative Distribution Function (CDF) of some data, it is not as easy to plot the PDF in python. Therefore I prepare this post serving as a cookbook for me and for others that may want to do the same thing.

Plotting a PDF is actually a problem of Kernel Density Estimation (KDE). This post will be focusing on plotting PDF in python and hence will not talk much about the theory of KDE. Interested readers are encouraged to read [this fantastic post](https://jakevdp.github.io/blog/2013/12/01/kernel-density-estimation/) about kernel density estimation in python.

### Simulation data
The data used consist of 10,000 data points sampled from two normal distributions with 5,000 from each. The simulation data are generated from the following code.
```python
import numpy as np


size = 5000
np.random.seed(11)
data1 = np.random.normal(-3,2,size)
data2 = np.random.normal(7,3,size)
data = np.append(data1, data2)
```

Histogram of the original data is shown below:
```python
import matplotlib.pyplot as plt


fig, ax = plt.subplots(figsize=(6, 2))
ax.hist(data, bins=30)
ax.set_xlim([-10, 20])
ax.set_title('Histogram of Simulation Data', fontsize=10)
fig.tight_layout()
plt.show()
```
![Original data]({filename}/images/hist.png)
Now let's get into our business of how to plot probability density functions.

### 1. The easy way
Serveral python packages come with the capability of plotting PDF. They are easy to use and therefore suitable for those who are just interested to make a simple PDF plot.

#### PDF plots with `seaborn`
[`seaborn`](http://seaborn.pydata.org/index.html) is a powerful python visualization library based on `matplotlib`. `Seaborn comes with the several functions that are very handy for making PDF plots.

The `seaborn.distplot` function is the easiest way to make a PDF plot for a data set. It also shows the histogram by default. The users may toggle the histogram using the `kde` argument.

```python
import seaborn as sns


fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 4))     
sns.distplot(data, hist=True, ax=ax1)                          # Histogram can be toggled by setting hist=False
ax1.grid(False)
ax1.set_xlim([-10, 20])
ax1.set_ylim([0, 0.1])
ax1.set_title('KDE with Gaussian kernel', fontsize=10)

sns.distplot(data, norm_hist=True, ax=ax2, kde=False)          # Only show the histogram
sns.kdeplot(data, kernel='cos', bw='silverman', ax=ax2)        # Draw pdf with Cosine kernel, silverman bw method         
ax2.grid(False)
ax2.set_xlim([-10, 20])
ax2.set_ylim([0, 0.1])
ax2.set_title('KDE with Cosine kernel', fontsize=10)
fig.tight_layout()
plt.show()
```
![seaborn]({filename}/images/distplot.png)
`seaborn.distplot` only comes with the gaussian kernel for KDE. If another is of interest to the user, the `seaborn.kdeplot` function can be used. `seaborn.kdeplot` provides more options than`distplot` as well as more kernels including *Triangular*, *Cosine*, *Biweight*, etc. It also allows for several methods for bandwith selection.

#### PDF plots with `pandas`
Another library that comes with the capability of kernel density estimation is `pandas`. `pandas` is a very powerful and probably the most popular python library for data manipulatoin. It also comes with handy function for its `DataFrame` object. The result of the code looks very similar to the top panel of the previous figure and hence is not shown here.

```python
import pandas as pd


df = pd.DataFrame(data)
fig, ax = plt.subplots(figsize=(6, 2))
df.plot(kind='kde', ax=ax)       # This line is equivalent to " df.plot.kde(ax=ax) "
ax.set_xlim([-10, 20])
ax.set_title('KDE plot with pandas', fontsize=10)
plt.show()
```

### 2. The flexible way
One major disadvantage of `seaborn` and `pandas` is that they return a `matplotlib` `axis` project. Therefore we lost control of the curve we draw. It is fine if our object is just to plot the KDE curve. We often want more than that, however. For example, we may want to highlight the 90% confidence interval. If this is the case, we should take a look at a slightly more complex way of plotting KDE curves that gives us more control over our figure.

#### KDE plot with `scipy`

`scipy` is a famous python library for scientific computation. KDE plots can be easily made with `scipy.stats.gaussian_kde` class. One feature of `scipy.stats.gaussian_kde` is that it enables sampling of the estimated PDF.

```python
from scipy import stats


pdf = stats.gaussian_kde(data)
x = np.linspace(-10, 20, 2000)
y = pdf(x)
sample = pdf.resample(2000)
fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(6, 4))
ax1.plot(x, y)
ax1.hist(data, normed=True, bins=30)
ax1.set_title('PDF with histogram of original data', fontsize=10)
ax2.plot(x, y)
ax2.hist(sample[0], normed=True, bins=30)
ax2.set_title('PDF with historgram of resampled data', fontsize=10)
fig.tight_layout()
plt.show()
```
![scipy]({filename}/images/scipy_resampling.png)

#### KDE plot with `statsmodels`
`scipy.stats` suffers from one disvantages of having only one kernel - gaussian kernel. It is sufficient for most cases though. If the reader wants to use another kernel, then `statsmodels` is probably a good choice with seven kernels.
```python
from statsmodels.nonparametric.kde import KDEUnivariate


kde = KDEUnivariate(data)
kde.fit()
fig = plt.figure()
ax1 = fig.add_subplot(211)
ax1.plot(kde.support, kde.density, lw=2)
ax1.hist(data, bins=30, normed=True)
ax1.set_title('PDF with histogram', fontsize=10)
ax2 = fig.add_subplot(212)
ax2.plot(kde.support, kde.cdf, lw=2)
ax2.set_title('CDF', fontsize=10)
fig.tight_layout()
plt.show()
```
![stats]({filename}/images/stats_cdf_with_pdf.png)

However, things become a little complicated when we want to highlight the 80% confidence interval. We must first calculate the corresponding x values for this interval. These values should be calculated from the cumulative distribution function (CDF). The `KDEUnivariate` has an attribuate `cdf` that contains CDF value for the support. Hence we then use then `interp1d` function in `scipy.interpolate` to interpolate the inverse function of the cumulative distribution function to calculate the confidence intervals. If we want to use other scipy to estimate the PDF, for which there is no CDF function readily available, we may use the `ECDF` function in the `statsmodels.distributions.empirical_distribution` library to calculate the CDF. It returns the cumulative distribution function values at discrete x values. One advantage of using `ECDF` over `KDEUnivariate` is that it is much faster to intepolate using the former, probably due to the smaller size of the returned numpy array. The following code shows how to calculate confidence interval with `scipy.stats.gaussian_kde`, the same method can be used with `KDEUnivariate`.

```python
from statsmodels.distributions.empirical_distribution import ECDF
from scipy.interpolate import interp1d
from scipy.stats import gaussian_kde
kde = gaussian_kde(data)
ecdf = ECDF(data)
inv_cdf = interp1d(ecdf.y, ecdf.x)
x = np.arange(-10, 20, 0.01)
y = kde(x)
fig= plt.figure(figsize=(6, 4))
ax1 = fig.add_subplot(211)
ax1.plot(x, y, lw=2)
ax1.fill_between(x, y, where=(x > inv_cdf(.1)) & (x < inv_cdf(.9)), facecolor='r', alpha=.3)
ax1.set_title('Probability density function', fontsize=10)
ax2 = fig.add_subplot(212)
ax2.plot(ecdf.x, ecdf.y)
ax2.set_xlim([-10, 20])
for p in [0.1, 0.9]:
    ax2.plot([-10, inv_cdf(p)], [p, p], linestyle='dashed', lw=1, color='r')
    ax2.plot([inv_cdf(p), inv_cdf(p)], [0, p], linestyle='dashed', lw=1, color='r')
ax2.set_title('Cumulative Distribution Function', fontsize=10)
fig.tight_layout()
plt.show()
```
![scipy with cdf]({filename}/images/scipy_with_cdf.png)


To summarize, python provides several libraries that can be used to plot probability density functions. Libraries like `pandas` and `seaborn` are easy use while other packages `scipy.stats` and `statsmodels` offer more control over the plot. Readers can choose between these libraries based on their needs.
