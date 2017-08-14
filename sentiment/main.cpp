#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <math.h>
#include <time.h>

typedef unsigned int uint32_t;

uint32_t n;
uint32_t d = 3;
uint32_t k = 10;

double *point;

#define INFDIS (100000000.0)
#define eps	(100)

uint32_t *clst;
double *centre;
uint32_t *clst_size;

inline double sqr(double d) {
	return d * d;
}

inline double abs(double d) {
	if (d > 0) return d; else return -d;
}

inline double distance(const double *p, const double *q) {
	uint32_t i;
	double r;

	r = 0;
	for (i = 0; i < d; ++i)
		r += sqr(p[i] - q[i]);
	r = sqrt(r);

	return r;

}

static inline void read() {
	uint32_t i;
	uint32_t j;

	scanf("%u%u%u", &n, &d, &k);
	point = (double *)malloc(n * d * sizeof(double));
	for (i = 0; i < n; ++i)
		for (j = 0; j < d; ++j)
			scanf("%lf", &point[i * d + j]);
}

void set(uint32_t _n, uint32_t _d, uint32_t _k, const char *const *dat) {
	uint32_t i; uint32_t j;

	n = _n;
	d = _d;
	k = _k;

	point = (double *)malloc(n * d * sizeof(double));
	for (i = 0; i < n; ++i)
		for (j = 0; j < d; ++j)
			point[i * d + j] = (double)dat[i][j];
}

void chief() {
	uint32_t i;
	uint32_t j;
	uint32_t c;
	uint32_t l;

	double min_cr, max_cr;
	double old_sum_dis, new_sum_dis;
	double min_dis, dis;

	centre = (double *)malloc(k * d * sizeof(double));
	srand(time(NULL));
	j = 0;
	for (i = 0; i < n; ++i){
		c = rand() % (n - i);
		if (c + j < k){
			for (l = 0; l < d; ++l)
				centre[j * d + l] = (double)point[i * d + l];
			if (++j == k) break;
		}
	}

	clst_size = (uint32_t *)malloc(k * sizeof(uint32_t));

	clst = (uint32_t *)malloc(n * sizeof(uint32_t));
	
	old_sum_dis = INFDIS;
	while (1) {
		new_sum_dis = 0;
		for (i = 0; i < n; ++i) {
			min_dis = INFDIS;
			for (j = 0; j < k; ++j) {
				dis = distance(&point[i * d], &centre[j * d]);
				if (dis < min_dis) {
					min_dis = dis;
					c = j;
				}
			}
			clst[i] = c;
			new_sum_dis += min_dis;
		}
		if (abs(old_sum_dis - new_sum_dis) < eps) break;

		for (i = 0; i < k; ++i) {
			for (j = 0; j < d; ++j)
				centre[i * d + j] = 0;
			clst_size[i] = 0;
		}
		for (i = 0; i < n; ++i) {
			c = clst[i];
			for (j = 0; j < d; ++j)
				centre[c * d + j] += point[i * d + j];
			++clst_size[c];
		}
		for (i = 0; i < k; ++i)
			for (j = 0; j < d; ++j)
				centre[i * d + j] /= clst_size[i];

		old_sum_dis = new_sum_dis;
	}

	free(clst_size);
}

static inline void write() {
	uint32_t i, c;
	uint32_t j;

	for (i = 0; i < n; ++i) {
		c = clst[i];
		/*for (j = 0; j < d; ++j) {
			if (j > 0) putchar(' ');
			printf("%f", centre[c * d + j]);
		}*/
		printf("%d", c) ;
		putchar('\n');
	}

	free(centre);
	free(clst);
	free(point);
}

void get(char *const *dat) {
	uint32_t i;
	uint32_t c;
	uint32_t j;

	for (i = 0; i < n; ++i) {
		c = clst[i];
		for (j = 0; j < d; ++j)
			dat[i][j] = (char)centre[c * d + j];
	}

	free(centre);
	free(clst);
	free(point);
}

int main()
{
	freopen("k2u.txt", "r", stdin) ;
	freopen("keygroup.txt", "w", stdout) ;
	read() ;
	chief();
	write() ;
}
