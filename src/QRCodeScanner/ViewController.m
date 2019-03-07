//
//  ViewController.m
//  QRCodeScanner
//
//  Created by ervinchen on 2019/3/7.
//  Copyright © 2019年 ccnyou. All rights reserved.
//

#import "ViewController.h"
#import "WSLNativeScanTool.h"
#import "WSLScanView.h"
#import "QRCodeViewController.h"

@interface ViewController ()<UIImagePickerControllerDelegate, UINavigationControllerDelegate>
@property (nonatomic, strong) WSLNativeScanTool *scanTool;
@property (nonatomic, strong) WSLScanView *scanView;
@property (nonatomic, strong) NSString *scanResult;
@end

@implementation ViewController

#define _T(x) @(x)

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view.
    [self _initAppearance];
    [self _initScanTools];
}

- (void)viewDidAppear:(BOOL)animated {
    [super viewDidAppear:animated];

    [self.scanView finishedHandle];
    [self.scanTool sessionStartRunning];
    [self.scanView startScanAnimation];
}

- (void)_initAppearance {
    self.title = _T("扫描中...");
    self.view.backgroundColor = [UIColor blueColor];
    UIBarButtonItem *rightButton = [[UIBarButtonItem alloc] initWithTitle:_T("相册")
                                                                    style:UIBarButtonItemStylePlain
                                                                   target:self
                                                                   action:@selector(onRightTouched:)];
    self.navigationItem.rightBarButtonItem = rightButton;
}

- (void)_initScanTools {
    // 输出流视图
    UIView *preview = [[UIView alloc] initWithFrame:self.view.bounds];
    [self.view addSubview:preview];

    // 构建扫描样式视图
    __weak typeof(self) wself = self;
    self.scanView = [[WSLScanView alloc] initWithFrame:self.view.bounds];
    self.scanView.scanRetangleRect = CGRectMake(60, 120, (self.view.frame.size.width - 2 * 60), (self.view.frame.size.width - 2 * 60));
    self.scanView.colorAngle = [UIColor greenColor];
    self.scanView.photoframeAngleW = 20;
    self.scanView.photoframeAngleH = 20;
    self.scanView.photoframeLineW = 2;
    self.scanView.isNeedShowRetangle = YES;
    self.scanView.colorRetangleLine = [UIColor whiteColor];
    self.scanView.notRecoginitonArea = [UIColor colorWithRed:0 green:0 blue:0 alpha:0.5];
    self.scanView.animationImage = [UIImage imageNamed:@"scanLine"];
    self.scanView.flashSwitchBlock = ^(BOOL open) {
        [wself.scanTool openFlashSwitch:open];
    };
    [self.view addSubview:self.scanView];

    // 初始化扫描工具
    self.scanTool = [[WSLNativeScanTool alloc] initWithPreview:preview
                                                  andScanFrame:self.scanView.scanRetangleRect];
    self.scanTool.scanFinishedBlock = ^(NSString *scanString) {
        __strong typeof(wself) sself = wself;
        if (sself.scanResult) {
            return;
        }

        [sself _onScanString:scanString];
    };

    self.scanTool.monitorLightBlock = ^(float brightness) {
        if (brightness < 0) {
            // 环境太暗，显示闪光灯开关按钮
            [wself.scanView showFlashSwitch:YES];
        } else if (brightness > 0) {
            // 环境亮度可以,且闪光灯处于关闭状态时，隐藏闪光灯开关
            if (!wself.scanTool.flashOpen) {
                [wself.scanView showFlashSwitch:NO];
            }
        }
    };
}

- (void)_onScanString:(NSString *)scanString {
    if (@available(iOS 10.0, *)) {
        UIImpactFeedbackGenerator *feedbackGenerator = [[UIImpactFeedbackGenerator alloc] initWithStyle:UIImpactFeedbackStyleMedium];
        [feedbackGenerator impactOccurred];
    }

    self.scanResult = scanString;
    [self.scanView handlingResultsOfScan];
    [self.scanTool sessionStopRunning];
    [self.scanTool openFlashSwitch:NO];

    QRCodeViewController *controller = [[QRCodeViewController alloc] init];
    controller.code = scanString;
    [self.navigationController pushViewController:controller animated:YES];
}

- (void)onRightTouched:(id)sender {
    UIImagePickerController *imagePicker = [[UIImagePickerController alloc] init];
    imagePicker.sourceType = UIImagePickerControllerSourceTypePhotoLibrary;
    imagePicker.delegate = self;
    [self presentViewController:imagePicker animated:YES completion:nil];
}

#pragma mark - Image Picker

- (void)imagePickerController:(UIImagePickerController *)picker didFinishPickingMediaWithInfo:(NSDictionary *)info {
    NSString *type = [info objectForKey:UIImagePickerControllerMediaType];
    if ([type isEqualToString:@"public.image"]) {
        NSString *key = nil;
        if (picker.allowsEditing) {
            key = UIImagePickerControllerEditedImage;
        } else {
            key = UIImagePickerControllerOriginalImage;
        }

        UIImage *image = [info objectForKey:key];
        [self.scanTool scanImageQRCode:image];
        [picker dismissViewControllerAnimated:YES completion:nil];
    }
}

- (void)imagePickerControllerDidCancel:(UIImagePickerController *)picker {
    [picker dismissViewControllerAnimated:YES completion:nil];
}

@end
