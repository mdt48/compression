
from Quanitzer import UniformQuantizer, SemiUniformQuantizer, MaxLloydQuantizer
import utils

path = './HW3/image.gif'

image, vectorized_image = utils.open_vectorize_image(path)
print('\n\n***PART A***\n\n')
print('ENTROPY OF IMAGE={}'.format(utils.ENT(vectorized_image)))

print('\n\n***PART B***\n\n')
Q = UniformQuantizer(8, vectorized_image)

G_u_prime = Q.quantize()
print('ENTROPY OF G_prime={}'.format(utils.ENT(G_u_prime)))

G_u_hat = Q.dequantize(G_u_prime)
print('G_u_hat={}'.format(G_u_hat))

u_snr = utils.SNR(vectorized_image, G_u_hat)
print('SNR OF G_u_hat={}'.format(u_snr))


print('\n\n***PART C***\n\n')

Q = SemiUniformQuantizer(8, vectorized_image)
G_su_prime = Q.quantize()
print('ENTROPY OF G_prime={}'.format(utils.ENT(G_su_prime)))

G_su_hat = Q.dequantize(G_su_prime)
print('G_su_hat={}'.format(G_su_hat))

su_snr = utils.SNR(vectorized_image, G_su_hat)
print('SNR OF G_u_hat={}'.format(su_snr))


print('\n\n***PART D***\n\n')
Q = MaxLloydQuantizer(8, vectorized_image)



Q.fit()

G_op_prime = Q.quantize()
print('ENTROPY OF G_op_prime={}'.format(utils.ENT(G_op_prime)))

G_op_hat = Q.dequantize(G_op_prime)
print('G_op_hat={}'.format(G_op_hat))

op_snr = utils.SNR(vectorized_image, G_op_hat)
print('SNR OF G_op_hat={}'.format(op_snr))