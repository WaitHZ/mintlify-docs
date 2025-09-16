import argparse
from ast import arguments, literal_eval
import os
from tqdm import tqdm
import json
import re


icon_map = {
    "arxiv_local": '<svg width="14" height="14" viewBox="0 0 17.732 24.269" style={{margin: 0, padding: 0, display: \'inline-block\'}}><path fill="#bdb9b4" d="m6.565 9.368 2.266 2.738 6.674-7.84c.353-.47.52-.717.353-1.117a1.218 1.218 0 0 0-1.061-.748.953.953 0 0 0-.712.262Z"/><path fill="#b31b1b" d="M12.541 10.677 1.935.503a1.413 1.413 0 0 0-.834-.5 1.09 1.09 0 0 0-1.027.66c-.167.4-.047.681.319 1.206l8.44 10.242-6.282 7.716a1.336 1.336 0 0 0-.323 1.3 1.114 1.114 0 0 0 1.04.69.992.992 0 0 0 .748-.365l8.519-7.92a1.924 1.924 0 0 0 .006-2.855Z"/><path fill="#bdb9b4" d="M17.336 22.364 8.811 12.089 6.546 9.352l-1.389 1.254a2.063 2.063 0 0 0 0 2.965L15.969 23.99a.925.925 0 0 0 .742.282 1.039 1.039 0 0 0 .953-.667 1.261 1.261 0 0 0-.328-1.241Z"/></svg>',
    "filesystem": '<svg xmlns="http://www.w3.org/2000/svg"  viewBox="0 0 48 48" width="14px" height="14px" style={{margin: 0, padding: 0, display: \'inline-block\'}}><path fill="#FFA000" d="M40,12H22l-4-4H8c-2.2,0-4,1.8-4,4v8h40v-4C44,13.8,42.2,12,40,12z"/><path fill="#FFCA28" d="M40,12H8c-2.2,0-4,1.8-4,4v20c0,2.2,1.8,4,4,4h32c2.2,0,4-1.8,4-4V16C44,13.8,42.2,12,40,12z"/></svg>',
    "scholarly": '<svg xmlns="http://www.w3.org/2000/svg"  viewBox="0 0 48 48" width="14px" height="14px" style={{margin: 0, padding: 0, display: \'inline-block\'}}><path fill="#1e88e5" d="M24,4C12.954,4,4,12.954,4,24s8.954,20,20,20s20-8.954,20-20S35.046,4,24,4z"/><path fill="#1565c0" d="M35,16.592v-3.878L37,11H27l0.917,1.833c-1.236,0-2.265,0-2.265,0S19.095,13,19.095,18.748	c0,5.752,5.732,5.088,5.732,5.088s0,0.865,0,1.453c0,0.594,0.77,0.391,0.864,1.583c-0.388,0-7.964-0.208-7.964,4.998	s6.679,4.959,6.679,4.959s7.722,0.365,7.722-6.104c0-3.871-4.405-5.121-4.405-6.686c0-1.563,3.319-2.012,3.319-5.684	c0-0.823-0.028-1.524-0.149-2.12L34,13.571v3.02c-0.581,0.207-1,0.756-1,1.408v4.5c0,0.829,0.672,1.5,1.5,1.5s1.5-0.671,1.5-1.5V18	C36,17.348,35.581,16.799,35,16.592z M30.047,31.169c0.131,2.024-1.929,3.811-4.603,3.998c-2.671,0.188-4.946-1.295-5.077-3.316	c-0.133-2.016,1.927-3.805,4.6-3.996C27.641,27.667,29.914,29.152,30.047,31.169z M26.109,22.453	c-1.592,0.451-3.375-1.062-3.982-3.367c-0.604-2.312,0.195-4.543,1.786-4.992c1.593-0.453,3.374,1.059,3.981,3.367	C28.499,19.77,27.702,22.004,26.109,22.453z"/><path fill="#e8eaf6" d="M34,16.592V12c0-0.051-0.015-0.097-0.029-0.143L35,11H21l-9,8h5.383	c0.174,5.466,5.715,4.836,5.715,4.836s0,0.865,0,1.453c0,0.594,0.771,0.391,0.865,1.583c-0.388,0-7.964-0.208-7.964,4.998	s6.679,4.959,6.679,4.959s7.721,0.365,7.721-6.104c0-3.871-4.404-5.121-4.404-6.686c0-1.563,3.318-2.012,3.318-5.684	c0-0.971-0.047-1.763-0.232-2.422L33,12.667v3.925c-0.581,0.207-1,0.756-1,1.408v4.5c0,0.829,0.672,1.5,1.5,1.5s1.5-0.671,1.5-1.5	V18C35,17.348,34.581,16.799,34,16.592z M28.319,31.169c0.131,2.024-1.928,3.811-4.602,3.998c-2.671,0.188-4.946-1.295-5.077-3.316	c-0.133-2.016,1.927-3.805,4.599-3.996C25.914,27.667,28.187,29.152,28.319,31.169z M24.38,22.453	c-1.591,0.451-3.373-1.062-3.981-3.367c-0.604-2.312,0.194-4.543,1.785-4.992c1.593-0.453,3.374,1.059,3.982,3.367	C26.77,19.77,25.973,22.004,24.38,22.453z"/></svg>',
    "claim_done": '<svg width="14px" height="14px" viewBox="0 0 1024 1024" version="1.1" xmlns="http://www.w3.org/2000/svg" style={{margin: 0, padding: 0, display: \'inline-block\'}}><path d="M861.588238 240.133873v-65.792823c0-36.191275-29.439775-65.631049-65.631049-65.63105h-21.877358c-36.191275 0-65.631049 29.439775-65.631049 65.63105v65.631049H314.659414v-65.631049c0-36.191275-29.439775-65.631049-65.631049-65.63105h-21.877358c-36.191275 0-65.631049 29.439775-65.631049 65.63105v65.792823c-36.317212 0.868255-65.631049 30.539428-65.63105 67.061417v543.745565c0 37.06772 30.155471 67.223191 67.223191 67.223191h696.886045c37.06772 0 67.223191-30.155471 67.223191-67.223191V307.19529c-0.001024-36.52199-29.315885-66.193162-65.633097-67.061417z m-109.385765-65.792823c0-12.060345 9.817012-21.877358 21.877358-21.877358h21.877358c12.060345 0 21.877358 9.817012 21.877358 21.877358v175.016814c0 12.060345-9.817012 21.877358-21.877358 21.877358h-21.877358c-12.060345 0-21.877358-9.817012-21.877358-21.877358V174.34105z m-546.928824 0c0-12.060345 9.817012-21.877358 21.877358-21.877358h21.877358c12.060345 0 21.877358 9.817012 21.877358 21.877358v175.016814c0 12.060345-9.817012 21.877358-21.877358 21.877358h-21.877358c-12.060345 0-21.877358-9.817012-21.877358-21.877358V174.34105z m678.191947 676.600829c0 12.935767-10.532708 23.468476-23.468476 23.468475H163.111076c-12.935767 0-23.468476-10.532708-23.468476-23.468475V307.19529c0-12.402323 9.677764-22.593054 21.877358-23.415233v65.577807c0 36.191275 29.439775 65.631049 65.631049 65.631049h21.877358c36.191275 0 65.631049-29.439775 65.631049-65.631049v-65.631049h393.789368v65.631049c0 36.191275 29.439775 65.631049 65.631049 65.631049h21.877358c36.191275 0 65.631049-29.439775 65.631049-65.631049v-65.577807c12.19857 0.82218 21.877358 11.012911 21.877358 23.415233v543.746589z" fill="#22C67F" /><path d="M706.719439 478.272194l-48.01715-44.741741-182.28128 195.621482-111.468348-122.615387-48.563905 44.148911 159.469116 172.685427z" fill="#74E8AE" /></svg>',
    "playwright_with_chunk": '<svg xmlns="http://www.w3.org/2000/svg"  viewBox="0 0 48 48" width="14px" height="14px" style={{margin: 0, padding: 0, display: \'inline-block\'}}><path fill="#4caf50" d="M44,24c0,11.044-8.956,20-20,20S4,35.044,4,24S12.956,4,24,4S44,12.956,44,24z"/><path fill="#ffc107" d="M24,4v20l8,4l-8.843,16c0.317,0,0.526,0,0.843,0c11.053,0,20-8.947,20-20S35.053,4,24,4z"/><path fill="#4caf50" d="M44,24c0,11.044-8.956,20-20,20S4,35.044,4,24S12.956,4,24,4S44,12.956,44,24z"/><path fill="#ffc107" d="M24,4v20l8,4l-8.843,16c0.317,0,0.526,0,0.843,0c11.053,0,20-8.947,20-20S35.053,4,24,4z"/><path fill="#f44336" d="M41.84,15H24v13l-3-1L7.16,13.26H7.14C10.68,7.69,16.91,4,24,4C31.8,4,38.55,8.48,41.84,15z"/><path fill="#dd2c00" d="M7.158,13.264l8.843,14.862L21,27L7.158,13.264z"/><path fill="#558b2f" d="M23.157,44l8.934-16.059L28,25L23.157,44z"/><path fill="#f9a825" d="M41.865,15H24l-1.579,4.58L41.865,15z"/><path fill="#fff" d="M33,24c0,4.969-4.031,9-9,9s-9-4.031-9-9s4.031-9,9-9S33,19.031,33,24z"/><path fill="#2196f3" d="M31,24c0,3.867-3.133,7-7,7s-7-3.133-7-7s3.133-7,7-7S31,20.133,31,24z"/></svg>',
    "excel": '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 48 48" width="14" height="14" style={{margin: 0, padding: 0, display: \'inline-block\'}}><path fill="#169154" d="M29,6H15.744C14.781,6,14,6.781,14,7.744v7.259h15V6z"/><path fill="#18482a" d="M14,33.054v7.202C14,41.219,14.781,42,15.743,42H29v-8.946H14z"/><path fill="#0c8045" d="M14 15.003H29V24.005000000000003H14z"/><path fill="#17472a" d="M14 24.005H29V33.055H14z"/><g><path fill="#29c27f" d="M42.256,6H29v9.003h15V7.744C44,6.781,43.219,6,42.256,6z"/><path fill="#27663f" d="M29,33.054V42h13.257C43.219,42,44,41.219,44,40.257v-7.202H29z"/><path fill="#19ac65" d="M29 15.003H44V24.005000000000003H29z"/><path fill="#129652" d="M29 24.005H44V33.055H29z"/></g><path fill="#0c7238" d="M22.319,34H5.681C4.753,34,4,33.247,4,32.319V15.681C4,14.753,4.753,14,5.681,14h16.638 C23.247,14,24,14.753,24,15.681v16.638C24,33.247,23.247,34,22.319,34z"/><path fill="#fff" d="M9.807 19L12.193 19 14.129 22.754 16.175 19 18.404 19 15.333 24 18.474 29 16.123 29 14.013 25.07 11.912 29 9.526 29 12.719 23.982z"/></svg>',
    "terminal": '<svg xmlns="http://www.w3.org/2000/svg"  viewBox="0 0 48 48" width="14px" height="14px" style={{margin: 0, padding: 0, display: \'inline-block\'}}><path fill="#0277bd" d="M19.847,41.956c-5.629-0.002-11.259,0.024-16.888-0.013c-2.855-0.019-3.374-0.7-2.731-3.525 c2.178-9.58,4.427-19.143,6.557-28.734C7.356,7.112,8.588,5.975,11.312,6C22.57,6.106,33.829,6.034,45.088,6.046 c2.824,0.003,3.298,0.614,2.664,3.511c-2.058,9.406-4.129,18.809-6.236,28.203c-0.789,3.516-1.697,4.187-5.353,4.195 C30.724,41.966,25.285,41.958,19.847,41.956z"/><path fill="#fafafa" d="M25.057 23.922c-.608-.687-1.114-1.267-1.531-1.732-2.43-2.728-4.656-5.27-7.063-7.869-1.102-1.189-1.453-2.344-.13-3.518 1.307-1.16 2.592-1.058 3.791.277 3.34 3.717 6.676 7.438 10.071 11.104 1.268 1.369.972 2.3-.424 3.315-5.359 3.895-10.687 7.833-16.01 11.778-1.196.887-2.337 1.109-3.304-.201-1.066-1.445-.08-2.305 1.026-3.114 3.955-2.893 7.903-5.798 11.834-8.725C23.865 24.83 24.595 24.267 25.057 23.922zM21.75 37C20.625 37 20 36 20 35s.625-2 1.75-2c4.224 0 6.112 0 9.5 0 1.125 0 1.75 1 1.75 2s-.625 2-1.75 2C29.125 37 25 37 21.75 37z"/></svg>',
    "web_search": '<svg height="14" width="14" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 512 512" style={{margin: 0, padding: 0, display: \'inline-block\'}}><g fill="none" fill-rule="evenodd"><rect fill="#fabc05" height="512" rx="42.667" width="512"/><path d="M58.667 293.333L0 209.125V42.663C0 19.1 19.137 0 42.663 0h426.674C492.9 0 512 19.137 512 42.663l-282.667.004S58.667 305.14 58.667 293.333z" fill="#eb4335"/><path d="M303.3 340.528L199.876 512H42.633C19.087 512 0 492.94 0 469.328V209.125l54.537 74.854c28.457 48.33 81.024 80.762 141.167 80.762 40.548 0 77.822-14.86 106.533-39.29l5.348 5.349c-.918 3.235-2.337 6.5-4.284 9.728z" fill="#34a854"/><g fill-rule="nonzero"><path d="M194.667 85.333c-66.667 0-120 52.148-120 117.334C74.667 267.852 128 320 194.667 320c66.666 0 120-52.148 120-117.333 0-65.186-53.334-117.334-120-117.334z" fill="#4285f5"/><path d="M327.59 300.924l28.788 28.787 13.204-14.159 115.751 115.751-59.363 59.364-115.751-115.751 13.553-12.64-28.85-28.85c-27.526 20.496-61.677 32.712-98.52 32.712C105.605 366.138 32 292.532 32 201.735c0-90.796 73.605-164.402 164.402-164.402s164.402 73.606 164.402 164.402c0 37.142-12.414 71.549-33.213 99.19zM196.403 87.92c-63.231 0-113.817 50.585-113.817 113.816 0 63.232 50.586 113.817 113.817 113.817S310.22 264.967 310.22 201.735c0-63.231-50.585-113.816-113.817-113.816z" fill="#fff"/></g></g></svg>',
    "pdf-tools": '<svg width="14px" height="14px" viewBox="-4 0 40 40" fill="none" xmlns="http://www.w3.org/2000/svg" style={{margin: 0, padding: 0, display: \'inline-block\'}}><path d="M25.6686 26.0962C25.1812 26.2401 24.4656 26.2563 23.6984 26.145C22.875 26.0256 22.0351 25.7739 21.2096 25.403C22.6817 25.1888 23.8237 25.2548 24.8005 25.6009C25.0319 25.6829 25.412 25.9021 25.6686 26.0962ZM17.4552 24.7459C17.3953 24.7622 17.3363 24.7776 17.2776 24.7939C16.8815 24.9017 16.4961 25.0069 16.1247 25.1005L15.6239 25.2275C14.6165 25.4824 13.5865 25.7428 12.5692 26.0529C12.9558 25.1206 13.315 24.178 13.6667 23.2564C13.9271 22.5742 14.193 21.8773 14.468 21.1894C14.6075 21.4198 14.7531 21.6503 14.9046 21.8814C15.5948 22.9326 16.4624 23.9045 17.4552 24.7459ZM14.8927 14.2326C14.958 15.383 14.7098 16.4897 14.3457 17.5514C13.8972 16.2386 13.6882 14.7889 14.2489 13.6185C14.3927 13.3185 14.5105 13.1581 14.5869 13.0744C14.7049 13.2566 14.8601 13.6642 14.8927 14.2326ZM9.63347 28.8054C9.38148 29.2562 9.12426 29.6782 8.86063 30.0767C8.22442 31.0355 7.18393 32.0621 6.64941 32.0621C6.59681 32.0621 6.53316 32.0536 6.44015 31.9554C6.38028 31.8926 6.37069 31.8476 6.37359 31.7862C6.39161 31.4337 6.85867 30.8059 7.53527 30.2238C8.14939 29.6957 8.84352 29.2262 9.63347 28.8054ZM27.3706 26.1461C27.2889 24.9719 25.3123 24.2186 25.2928 24.2116C24.5287 23.9407 23.6986 23.8091 22.7552 23.8091C21.7453 23.8091 20.6565 23.9552 19.2582 24.2819C18.014 23.3999 16.9392 22.2957 16.1362 21.0733C15.7816 20.5332 15.4628 19.9941 15.1849 19.4675C15.8633 17.8454 16.4742 16.1013 16.3632 14.1479C16.2737 12.5816 15.5674 11.5295 14.6069 11.5295C13.948 11.5295 13.3807 12.0175 12.9194 12.9813C12.0965 14.6987 12.3128 16.8962 13.562 19.5184C13.1121 20.5751 12.6941 21.6706 12.2895 22.7311C11.7861 24.0498 11.2674 25.4103 10.6828 26.7045C9.04334 27.3532 7.69648 28.1399 6.57402 29.1057C5.8387 29.7373 4.95223 30.7028 4.90163 31.7107C4.87693 32.1854 5.03969 32.6207 5.37044 32.9695C5.72183 33.3398 6.16329 33.5348 6.6487 33.5354C8.25189 33.5354 9.79489 31.3327 10.0876 30.8909C10.6767 30.0029 11.2281 29.0124 11.7684 27.8699C13.1292 27.3781 14.5794 27.011 15.985 26.6562L16.4884 26.5283C16.8668 26.4321 17.2601 26.3257 17.6635 26.2153C18.0904 26.0999 18.5296 25.9802 18.976 25.8665C20.4193 26.7844 21.9714 27.3831 23.4851 27.6028C24.7601 27.7883 25.8924 27.6807 26.6589 27.2811C27.3486 26.9219 27.3866 26.3676 27.3706 26.1461ZM30.4755 36.2428C30.4755 38.3932 28.5802 38.5258 28.1978 38.5301H3.74486C1.60224 38.5301 1.47322 36.6218 1.46913 36.2428L1.46884 3.75642C1.46884 1.6039 3.36763 1.4734 3.74457 1.46908H20.263L20.2718 1.4778V7.92396C20.2718 9.21763 21.0539 11.6669 24.0158 11.6669H30.4203L30.4753 11.7218L30.4755 36.2428ZM28.9572 10.1976H24.0169C21.8749 10.1976 21.7453 8.29969 21.7424 7.92417V2.95307L28.9572 10.1976ZM31.9447 36.2428V11.1157L21.7424 0.871022V0.823357H21.6936L20.8742 0H3.74491C2.44954 0 0 0.785336 0 3.75711V36.2435C0 37.5427 0.782956 40 3.74491 40H28.2001C29.4952 39.9997 31.9447 39.2143 31.9447 36.2428Z" fill="#EB5757"/></svg>',
    "google_map": '<svg xmlns="http://www.w3.org/2000/svg"  viewBox="0 0 48 48" width="14px" height="14px" style={{margin: 0, padding: 0, display: \'inline-block\'}}><path fill="#48b564" d="M35.76,26.36h0.01c0,0-3.77,5.53-6.94,9.64c-2.74,3.55-3.54,6.59-3.77,8.06	C24.97,44.6,24.53,45,24,45s-0.97-0.4-1.06-0.94c-0.23-1.47-1.03-4.51-3.77-8.06c-0.42-0.55-0.85-1.12-1.28-1.7L28.24,22l8.33-9.88	C37.49,14.05,38,16.21,38,18.5C38,21.4,37.17,24.09,35.76,26.36z"/><path fill="#fcc60e" d="M28.24,22L17.89,34.3c-2.82-3.78-5.66-7.94-5.66-7.94h0.01c-0.3-0.48-0.57-0.97-0.8-1.48L19.76,15	c-0.79,0.95-1.26,2.17-1.26,3.5c0,3.04,2.46,5.5,5.5,5.5C25.71,24,27.24,23.22,28.24,22z"/><path fill="#2c85eb" d="M28.4,4.74l-8.57,10.18L13.27,9.2C15.83,6.02,19.69,4,24,4C25.54,4,27.02,4.26,28.4,4.74z"/><path fill="#ed5748" d="M19.83,14.92L19.76,15l-8.32,9.88C10.52,22.95,10,20.79,10,18.5c0-3.54,1.23-6.79,3.27-9.3	L19.83,14.92z"/><path fill="#5695f6" d="M28.24,22c0.79-0.95,1.26-2.17,1.26-3.5c0-3.04-2.46-5.5-5.5-5.5c-1.71,0-3.24,0.78-4.24,2L28.4,4.74	c3.59,1.22,6.53,3.91,8.17,7.38L28.24,22z"/></svg>',
    "python-execute": '<svg width="14px" height="14px" viewBox="0 0 32 32" fill="none" xmlns="http://www.w3.org/2000/svg" style={{margin: 0, padding: 0, display: \'inline-block\'}}><path fillRule="evenodd" clipRule="evenodd" d="M13.0164 2C10.8193 2 9.03825 3.72453 9.03825 5.85185V8.51852H15.9235V9.25926H5.97814C3.78107 9.25926 2 10.9838 2 13.1111L2 18.8889C2 21.0162 3.78107 22.7407 5.97814 22.7407H8.27322V19.4815C8.27322 17.3542 10.0543 15.6296 12.2514 15.6296H19.5956C21.4547 15.6296 22.9617 14.1704 22.9617 12.3704V5.85185C22.9617 3.72453 21.1807 2 18.9836 2H13.0164ZM12.0984 6.74074C12.8589 6.74074 13.4754 6.14378 13.4754 5.40741C13.4754 4.67103 12.8589 4.07407 12.0984 4.07407C11.3378 4.07407 10.7213 4.67103 10.7213 5.40741C10.7213 6.14378 11.3378 6.74074 12.0984 6.74074Z" fill="#327EBD"/><path fillRule="evenodd" clipRule="evenodd" d="M18.9834 30C21.1805 30 22.9616 28.2755 22.9616 26.1482V23.4815L16.0763 23.4815L16.0763 22.7408L26.0217 22.7408C28.2188 22.7408 29.9998 21.0162 29.9998 18.8889V13.1111C29.9998 10.9838 28.2188 9.25928 26.0217 9.25928L23.7266 9.25928V12.5185C23.7266 14.6459 21.9455 16.3704 19.7485 16.3704L12.4042 16.3704C10.5451 16.3704 9.03809 17.8296 9.03809 19.6296L9.03809 26.1482C9.03809 28.2755 10.8192 30 13.0162 30H18.9834ZM19.9015 25.2593C19.1409 25.2593 18.5244 25.8562 18.5244 26.5926C18.5244 27.329 19.1409 27.9259 19.9015 27.9259C20.662 27.9259 21.2785 27.329 21.2785 26.5926C21.2785 25.8562 20.662 25.2593 19.9015 25.2593Z" fill="#FFDA4B"/></svg>',
    "memory": '<svg xmlns="http://www.w3.org/2000/svg" x="0px" y="0px" width="64" height="64" viewBox="0 0 48 48" style={{margin: 0, padding: 0, display: \'inline-block\'}}><path fill="#4A90E2" d="M8 6h32c1.105 0 2 0.895 2 2v32c0 1.105-0.895 2-2 2H8c-1.105 0-2-0.895-2-2V8c0-1.105 0.895-2 2-2z"/><path fill="#ffffff" d="M10 8h28v28H10V8z"/><path fill="#4A90E2" d="M12 10h24v2H12v-2z"/><path fill="#4A90E2" d="M12 14h24v2H12v-2z"/><path fill="#4A90E2" d="M12 18h24v2H12v-2z"/><path fill="#4A90E2" d="M12 22h24v2H12v-2z"/><path fill="#4A90E2" d="M12 26h24v2H12v-2z"/><path fill="#4A90E2" d="M12 30h24v2H12v-2z"/><path fill="#4A90E2" d="M12 34h24v2H12v-2z"/><path fill="#4A90E2" d="M6 4h2v4H6V4z"/><path fill="#4A90E2" d="M40 4h2v4h-2V4z"/><path fill="#4A90E2" d="M6 40h2v4H6v-4z"/><path fill="#4A90E2" d="M40 40h2v4h-2v-4z"/></svg>'
}

icon_cnt = len(icon_map)

icon_map["googlesearch"] = icon_map["web_search"]
icon_map["playwright"] = icon_map["playwright_with_chunk"]


def find_mdx_files_with_underscore(dir_path):
    mdx_files = []
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            if file.endswith("_.mdx"):
                mdx_files.append(os.path.join(root, file))
    return mdx_files


def clear(task_dir):
    for root, dirs, files in os.walk(task_dir):
        for file in files:
            if file.endswith("__.mdx"):
                file_path = os.path.join(root, file)
                try:
                    os.remove(file_path)
                    print(f"Deleted: {file_path}")
                except Exception as e:
                    print(f"Failed to delete {file_path}: {e}")


def raw_json_str_to_python(obj: str) -> dict:
    """
    把控制台里打印出来的“伪 JSON 字符串”还原成 Python 对象。
    1. 去掉首尾的引号（如果有）
    2. 把真正的 JSON 需要的转义补回去
    3. json.loads 解析
    """
    # 1. 去掉首尾可能被人手工包上的双引号
    obj = obj.strip()
    if (obj.startswith('"') and obj.endswith('"')) or \
       (obj.startswith("'") and obj.endswith("'")):
        obj = obj[1:-1]

    # 2. 把“用户眼里”的反斜杠变成“JSON 眼里”的反斜杠
    #    即：\n  -> \\n
    #        \" -> \\\"
    #        \\ -> \\\\
    obj = obj.encode('utf-8').decode('unicode_escape')   # 先解开 \n \t \"
    obj = obj.replace('\\', r'\\')                       # 再整体把反斜杠翻倍
    obj = obj.replace(r'\"', r'\"')                      # 把已经翻倍的 \" 还原

    # 3. 现在它是合法 JSON 字符串了
    return json.loads(obj)


def main(args):

    task_dir = args.task_dir

    clear(task_dir)

    mdx_files = find_mdx_files_with_underscore(task_dir)
    for f in tqdm(mdx_files):
        f_prefix = f.replace("_.mdx", "")
        print(f_prefix)
        target_md = f_prefix + ".mdx"
        print(target_md)

        with open(f, "r", encoding="utf-8") as src, open(target_md, "w", encoding="utf-8") as dst:
            dst.write(src.read())

            log_dir = f_prefix + "/"

            if len(os.listdir(log_dir)) > 0:
                dst.write(f"\n<AccordionGroup>\n")

            for log_file in sorted(os.listdir(log_dir)):
                if log_file.endswith(".json"):
                    log_path = os.path.join(log_dir, log_file)
                    with open(log_path, "r", encoding="utf-8") as lf:
                        log_data = json.load(lf)
                        msgs = log_data["messages"]
                        
                        model_name = log_path.split("/")[-1].replace(".json", "")
                        dst.write(f"<Accordion title=\"{model_name}\">\n\n")

                        dst.write("<Columns cols={3}>\n")
                        if log_data["pass"]:
                            dst.write(f"<Card title=\"Task Completion\" icon=\"check\">\n")
                            dst.write(f"Completed\n")
                        else:
                            dst.write(f"<Card title=\"Task Completion\" icon=\"x\">\n")
                            dst.write(f"Failed\n")
                        dst.write(f"</Card>\n")
                        dst.write(f"<Card title=\"Tool Calls\" icon=\"wrench\">\n")
                        tool_call_num = 0
                        for msg in msgs:
                            if msg["role"] == "assistant" and "tool_calls" in msg:
                                tool_call_num += len(msg["tool_calls"])
                        dst.write(f"{tool_call_num}\n")
                        dst.write(f"</Card>\n")
                        dst.write(f"<Card title=\"Turns\" icon=\"arrows-rotate\">\n")
                        assit_msgs = [msg for msg in msgs if msg["role"] == "assistant"]
                        dst.write(f"{len(assit_msgs)}\n")
                        dst.write(f"</Card>\n")
                        dst.write(f"</Columns>\n\n")

                        for msg in msgs:
                            if msg["role"] == "user":
                                continue
                            elif msg["role"] == "assistant":
                                if "tool_calls" in msg:
                                    if not (msg["content"] == "" or msg["content"] is None or msg["content"] == "null"):
                                        dst.write(f"<div className=\"thinking-box\">\n")
                                        dst.write(f"🧐`Agent`\n\n{msg['content'].strip()}\n</div>\n\n")

                                    for msg_tool_call in msg["tool_calls"]:
                                        if msg_tool_call['type'] == "function":
                                            if msg_tool_call['function']['name'] == "local-python-execute":
                                                dst.write(f"<div className=\"tool-call-box\">\n")
                                                dst.write(f"{icon_map["python-execute"]}`{msg_tool_call['function']['name']}`\n\n")
                                                arg_s = json.loads(msg_tool_call['function']['arguments'])
                                                dst.write(f"```python {arg_s['filename'] if 'filename' in arg_s else ''}\n")
                                                dst.write(f"{arg_s['code']}\n")
                                                dst.write(f"```\n")
                                                dst.write(f"</div>\n\n")
                                            elif msg_tool_call['function']['name'] == "filesystem-write_file":
                                                arg_s = json.loads(msg_tool_call['function']['arguments'])
                                                dst.write(f"<div className=\"tool-call-box\">\n")
                                                dst.write(f"{icon_map['filesystem']}`{msg_tool_call['function']['name']}`\n\n")
                                                dst.write(f"```text workspace/{arg_s['path'].split('/')[-1]}\n")
                                                dst.write(f"{arg_s['content']}\n")
                                                dst.write(f"```\n")
                                                dst.write(f"</div>\n\n")
                                            else:
                                                dst.write(f"<div className=\"tool-call-box\">\n")
                                                server_function_name = msg_tool_call['function']['name']
                                                if server_function_name.startswith("local"):
                                                    server_name = ''.join(server_function_name.split("-")[1:])
                                                    function_name = ""
                                                elif server_function_name.startswith("pdf-tools"):
                                                    server_name = "pdf-tools"
                                                    function_name = "".join(server_function_name.split("-")[2:])
                                                else:
                                                    server_name, function_name = server_function_name.split("-")
                                                dst.write(icon_map[server_name] if server_name in icon_map else "🛠")
                                                dst.write(f"`{server_name} {function_name}`\n\n")
                                                dst.write(f"```json\n")
                                                argu_s = msg_tool_call['function']['arguments'].strip()[1:-1].split(",")
                                                if len(argu_s) == 1 and argu_s[0] == "":
                                                    dst.write("{}\n")
                                                else:
                                                    dst.write("{\n")
                                                    for i, arg in enumerate(argu_s):
                                                        if i == 0:
                                                            dst.write(f"\t{arg}")
                                                        else:
                                                            dst.write(f",\n\t{arg}")
                                                    dst.write("\n}\n")
                                                dst.write(f"```\n")
                                                dst.write(f"</div>\n\n")
                                        else:
                                            raise NotImplementedError(f"Unsupported tool call type: {msg_tool_call['type']}")
                                else:
                                    dst.write(f"<div className=\"thinking-box\">\n")
                                    dst.write(f"🧐`Agent`\n\n{msg['content'].strip()}\n</div>\n\n")
                            elif msg["role"] == "tool":
                                if msg['content'] is not None:
                                    try:
                                        # tool_res.replace(r'\"', r'"')
                                        # tool_res.replace(r'\\n', r'\n')
                                        with open("_tmp", "w", encoding="utf-8") as f:
                                            print(msg['content'], file=f)
                                        tool_res = json.load(open("_tmp", "r", encoding="utf-8"))
                                        tool_res = tool_res["text"]
                                        tool_res = tool_res.replace('```', '')
                                    except:
                                        tool_res = msg['content']
                                        if tool_res.startswith('[') and tool_res.endswith(']'):
                                            tool_res = tool_res.replace('[{', '[\n{')
                                            tool_res = tool_res.replace('}]', '}\n]')
                                            tool_res = tool_res.replace('}, {', '},\n{')
                                            tool_res = tool_res.replace(r'\n', ' ')

                                    dst.write(f"<div className=\"result-box\">\n")
                                    dst.write(f"🔍`tool result`\n```json\n{tool_res}\n```\n</div>\n\n")
                                else:
                                    raise NotImplementedError("tool result doesn't have content")
                                    # dst.write(f"<div className=\"result-box\">\n")
                                    # dst.write("🔍`tool result`\n```json\n{}\n```\n</div>\n\n")
                            else:
                                raise NotImplementedError(f"Unsupported message role: {msg['role']}")

                        dst.write(f"</Accordion>\n\n")
            
            if len(os.listdir(log_dir)) > 0:
                dst.write(f"</AccordionGroup>\n")

    _tmp_path = os.path.join(os.path.dirname(__file__), "_tmp")
    try:
        os.remove(_tmp_path)
    except FileNotFoundError:
        print(f"File {_tmp_path} not found, don't need to remove")
    else:
        print(f"Removed file {_tmp_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--task_dir", type=str, default="docs/tasks")
    args = parser.parse_args()
    main(args)

    print("icon_cnt", icon_cnt)