import pandas as pd

class Transform:

    __dict__ = {
        'tmđt': 'thương mại điện tử',
        'tg': 'thế giới',
        'qg': 'quốc gia',
        'vn': 'việt nam',
        'tq': 'trung quốc',
        'hq': 'hàn quốc',
        'sx': 'sản xuất',
        'dn': 'doanh nghệp',
        'ct': 'chủ tịch',
        'cty': 'công ty',
        'hđqt': 'hội đồng quản trị',
        'cn': 'công nhân',
        'gđ': 'giám đốc',
        'sp': 'sản phẩm',
        'ts': 'tiến sĩ',
        'nckh': 'nghiên cứu khoa học',
        'đh': 'đại học',
        'ncs': 'nghiên cứu sinh',
        'gs': 'giáo sư',
        'xh': 'xã hội',
        'us': 'mỹ',
        'kt': 'kinh tế',
        'mk': 'mekong',
        'đbscl': 'đồng bằng sông cửu long',
        'tphcm': 'thành phố hồ chí minh',
        'tt': 'tổng thống',
        'k': 'không',
        'ko': 'không',
        '$': 'đô la',
        'usd': 'đô la',
        'dollar': 'đô la',
        'mil': 'triệu',
        'ngta': 'người ta',
        'fo': 'f0',
        'tr': 'triệu',
        'nvyt': 'nhân viên y tế',
        'mxh': 'mạng xã hội',
        'x': 'twitter',
        'j': 'gì',
        'hn': 'hà nội',
        'bhyt': 'bảo hiểm y tế',
        'bhxh': 'bảo hiểm xã hội',
        'bhtn': 'bảo hiểm thất nghiệp',
        'bh': 'bảo hiểm',
        'bv': 'bệnh viện',
        'bs': 'bác sĩ',
        'xn': 'xét nghiệm',
        'bn': 'bệnh nhân',
        'yt': 'y tế',
        'tncn': 'thu nhập cá nhân',
        'passport': 'hộ chiếu',
        'ph': 'phụ huynh',
        'hs': 'học sinh',
        'sv': 'sinh viên',
        'gv': 'giáo viên',
        'gd': 'giáo dục',
        'thpt': 'trung học phổ thông',
        'ptth': 'trung học phổ thông',
        'sgk': 'sách giá khoa',
        'nxb': 'nhà xuất bản',
        'sd': 'sử dụng',
        'thcs': 'trung học cơ sở',
        'bđs': 'bất động sản',
        'cx': 'cũng',
        'it': 'công nghệ thông tin',
        'cntt': 'công nghệ thông tin',
        'mt': 'máy tính',
        'nhứt': 'nhất',
        'gg': 'google',
        'nn': 'nhà nước',
        'cmt': 'bình luận',
        'comment': 'bình luận',
        'vd': 'ví dụ',
        'kh': 'khách hàng',
        'lđ': 'lao động',
        'nlđ': 'người lao động',
        'engineer': 'kĩ sư',
        'sing': 'singapore',
        'ng': 'người',
        'sg': 'sài gòn',
        'ntn': 'như thế nào',
        'lv': 'làm việc',
        'ta': 'tiếng anh',
        'dc': 'được',
        'tn': 'thu nhập',
        'nhnn': 'ngân hàng nhà nước',
        'ot': 'tăng ca',
        'tw': 'trung ương',
        'pccc': 'phòng cháy chữa cháy',
        'cccd': 'căn cước công dân',
        'mttq': 'mặt trận tổ quốc',
        'ubnd': 'ủy ban nhân dân',
        'or': 'hoặc',
        'nsx': 'nhà sản xuất',
        'tp': 'thành phố',
        'hcm': 'hồ chí minh',
        'đsct': 'đường sắt cao tốc',
        'metro': 'đường sắt đô thị',
        'p/s': '',
        'dnnn': 'doanh nghiệp nhà nước',
        'đhbk': 'đại học bách khoa',
        'dhbk': 'đại học bách khoa',
        'đhqg': 'đại học quốc gia',
        'nc': 'nước',
        'đna': 'đông nam á',
        'plrtn': 'phân loại rác thải',
        'qđ': 'quy định',
        'gtvt': 'giao thông vận tải',

    }

    def __init__(self, csv_file):
        self.csv_file = csv_file
        self.df = pd.read_csv(self.csv_file)

    # Loại bỏ dấu câu
    def _remove_punctuation(self):
        pass

    # Loại bỏ chữ viết hoa
    def _lowercase(self):
        pass

    # Loại bỏ từ viết tắt
    def _remove_abbreviations(self):
        pass

    def _comment_length(self):
        pass

    def process(self):
        self._remove_punctuation()
        self._lowercase()
        self._remove_abbreviations()
        return self.df