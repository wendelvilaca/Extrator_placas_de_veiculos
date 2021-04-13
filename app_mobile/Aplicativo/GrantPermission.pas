unit GrantPermission;

interface

uses
  System.Permissions, System.SysUtils;

type
  TGrantPermission = class
  private
    class var FInstance: TGrantPermission;
  private
    FPermissionCamera: string;
    FPErmissionReadExternalStorage: string;
    FPermissionWriteExternalStorage: string;
    FGrentRequested: TProc;
    procedure LocationPermissionRequestResult(Sender: TObject; const APermissions: TArray<string>; const AGrantResults: TArray<TPermissionStatus>);
    procedure DisplayRationale(Sender: TObject; const APermissions: TArray<string>; const APostRationaleProc: TProc);
    {$IFDEF ANDROID}
    procedure Toast(const Msg: string; Duration: Integer);
    {$ENDIF}
  public
    constructor Create();
    destructor Destroy(); override;

    procedure Request(AGrentRequested: TProc);

    class property Instance: TGrantPermission read FInstance;
  end;

implementation

uses
  System.UITypes,
  FMX.DialogService
{$IFDEF ANDROID}
  ,Androidapi.Jni.Os,
  Androidapi.Helpers,
  FMX.Helpers.Android,
  Android.JNI.Toast,
  Androidapi.JNI.JavaTypes
{$ENDIF}
;

{ TGrantPermission }

constructor TGrantPermission.Create;
begin
{$IFDEF ANDROID}
  FPermissionCamera := JStringToString(TJManifest_permission.JavaClass.CAMERA);
  FPermissionReadExternalStorage := JStringToString(TJManifest_permission.JavaClass.READ_EXTERNAL_STORAGE);
  FPermissionWriteExternalStorage := JStringToString(TJManifest_permission.JavaClass.WRITE_EXTERNAL_STORAGE);
{$ENDIF}
end;

destructor TGrantPermission.Destroy;
begin

  inherited;
end;

procedure TGrantPermission.DisplayRationale(Sender: TObject;
  const APermissions: TArray<string>; const APostRationaleProc: TProc);
begin
  TDialogService.ShowMessage('The app can show where you are on the map if you give it permission',
    procedure(const AResult: TModalResult)
    begin
      APostRationaleProc;
    end)
end;

procedure TGrantPermission.LocationPermissionRequestResult(Sender: TObject;
  const APermissions: TArray<string>;
  const AGrantResults: TArray<TPermissionStatus>);
begin
{$IFDEF ANDROID}
  var LIsGrant := (Length(AGrantResults) = 3)
    and (AGrantResults[0] = TPermissionStatus.Granted)
    and (AGrantResults[1] = TPermissionStatus.Granted)
    and (AGrantResults[2] = TPermissionStatus.Granted);

//  if LIsGrant then
//    Self.Toast('Permissões liberadas', TJToast.JavaClass.LENGTH_SHORT)
//  else
//    Self.Toast('Permissões bloqueadas', TJToast.JavaClass.LENGTH_SHORT);

  if LIsGrant then FGrentRequested();
{$ENDIF}
end;

procedure TGrantPermission.Request(AGrentRequested: TProc);
begin
  FGrentRequested := AGrentRequested;
  PermissionsService.RequestPermissions([
    FPermissionCamera,
    FPermissionReadExternalStorage,
    FPermissionWriteExternalStorage],
    LocationPermissionRequestResult,
    DisplayRationale);
end;

{$IFDEF ANDROID}
procedure TGrantPermission.Toast(const Msg: string; Duration: Integer);
begin
  CallInUiThread(
    procedure
    begin
      TJToast.JavaClass.makeText(
        TAndroidHelper.Context,
        StrToJCharSequence(msg),
        Duration).show
    end);
end;
{$ENDIF}

initialization
  TGrantPermission.FInstance := TGrantPermission.Create;

finalization
  TGrantPermission.FInstance.DisposeOf();

end.
