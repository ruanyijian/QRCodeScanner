//
//  QRCodeViewController.m
//  organic
//
//  Created by ervinchen on 2018/10/19.
//  Copyright © 2018年 ccnyou. All rights reserved.
//

#import "UIView+Toast.h"
#import "WSLNativeScanTool.h"
#import "QRCodeViewController.h"

@interface QRCodeViewController ()
@property (weak, nonatomic) IBOutlet UIImageView *codeImageView;
@property (weak, nonatomic) IBOutlet UITextView *textView;
@end

@implementation QRCodeViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    // Do any additional setup after loading the view from its nib.
    
    self.title = @"查看二维码";
    self.codeImageView.image = [WSLNativeScanTool createQRCodeImageWithString:self.code
                                                                      andSize:CGSizeMake(200, 200)
                                                                 andBackColor:[UIColor whiteColor]
                                                                andFrontColor:[UIColor blackColor]
                                                               andCenterImage:nil];
    self.textView.text = self.code;
    self.textView.layer.borderWidth = 1.0f / [UIScreen mainScreen].scale;
    self.textView.layer.borderColor = [UIColor lightGrayColor].CGColor;
    
    if ([self.code hasPrefix:@"http"]) {
        UIBarButtonItem *barButtonItem = [[UIBarButtonItem alloc] initWithTitle:@"打开链接"
                                                                          style:UIBarButtonItemStylePlain
                                                                         target:self
                                                                         action:@selector(onOpenTouched:)];
        self.navigationItem.rightBarButtonItem = barButtonItem;
    }
}

- (IBAction)onCopyTouched:(id)sender {
    UIPasteboard *pasteboard = [UIPasteboard generalPasteboard];
    pasteboard.string = self.textView.text;
    [self.view makeToast:@"已复制"];
}

- (void)onOpenTouched:(id)sender {
    [[UIApplication sharedApplication] openURL:[NSURL URLWithString:self.code]];
}

@end
