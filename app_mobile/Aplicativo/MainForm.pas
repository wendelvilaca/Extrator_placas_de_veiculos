unit MainForm;

interface

uses
  System.SysUtils, System.Types, System.UITypes, System.Classes, System.Variants,
  FMX.Types, FMX.Controls, FMX.Forms, FMX.Graphics, FMX.Dialogs,
  FMX.Controls.Presentation, FMX.StdCtrls, FMX.Layouts, FMX.ExtCtrls,
  System.Actions, FMX.ActnList, FMX.StdActns, FMX.MediaLibrary.Actions,
  FMX.Objects,
  Frame.PhotoOptions, Frame.HistoricoConsulta, Frame.ConnectionSettings;

type
  TForm1 = class(TForm)
    Layout1: TLayout;
    SpeedButton3: TSpeedButton;
    ActionList1: TActionList;
    TakePhotoFromCameraAction1: TTakePhotoFromCameraAction;
    AniIndicator1: TAniIndicator;
    ToolBar1: TToolBar;
    btnOptions: TButton;
    Label2: TLabel;
    Button1: TButton;
    TakePhotoFromLibraryAction1: TTakePhotoFromLibraryAction;
    procedure FormCreate(Sender: TObject);
    procedure TakePhotoFromCameraAction1DidFinishTaking(Image: TBitmap);
    procedure FormShow(Sender: TObject);
    procedure btnOptionsClick(Sender: TObject);
    procedure TakePhotoFromLibraryAction1DidFinishTaking(Image: TBitmap);
  private
    FQueryHistoryFrame: TQueryHistoryFrame;
    FPhotoOptionsFrame: TPhotoOptionsFrame;
    FConnectionSettingsFrame: TConnectionSettingsFrame;
  public
    { Public declarations }
  end;

var
  Form1: TForm1;

implementation

uses
  DataAccess.Initialize, GrantPermission;

{$R *.fmx}

{ TForm1 }

procedure TForm1.btnOptionsClick(Sender: TObject);
begin
  FConnectionSettingsFrame.Options;
end;

procedure TForm1.FormCreate(Sender: TObject);
begin
  TakePhotoFromCameraAction1.Enabled := false;
  TGrantPermission.Instance.Request(procedure
    begin
      TakePhotoFromCameraAction1.Enabled := true;
    end
  );
  TLocalDataAccessInitService.Initialize();
  FConnectionSettingsFrame := TConnectionSettingsFrame.Create(btnOptions);
  FConnectionSettingsFrame.Parent := Self;
  FQueryHistoryFrame := TQueryHistoryFrame.Create(Self);
  FQueryHistoryFrame.Parent := Self;
  FPhotoOptionsFrame := TPhotoOptionsFrame.Create(Self);
  FPhotoOptionsFrame.Parent := Self;
end;

procedure TForm1.FormShow(Sender: TObject);
begin
  {$IFDEF ANDROID}
  //TakePhotoFromCameraAction1.Enabled := TGrantPermission.Instance.IsGrant;
  {$ELSE}
  //FPhotoOptionsFrame.ShowFrame(nil);
  {$ENDIF}
end;

procedure TForm1.TakePhotoFromCameraAction1DidFinishTaking(Image: TBitmap);
begin
  FPhotoOptionsFrame.ShowFrame(Image);
end;

procedure TForm1.TakePhotoFromLibraryAction1DidFinishTaking(Image: TBitmap);
begin
  FPhotoOptionsFrame.ShowFrame(Image);
end;

end.
